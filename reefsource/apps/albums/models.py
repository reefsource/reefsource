import logging
import uuid
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel
from os.path import splitext

from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


def uploaded_file_to(instance, filename):
    """
    Determine where the uploaded file should go on the server.
    """
    filename = filename.split('/')[-1]

    try:
        ext = '.' + filename.split('.')[-1]
    except IndexError:
        ext = ''

    format_dict = {
        'user_id': instance.album.user.id,
        'album_id': instance.album.id,
        'date': timezone.now().strftime('%Y/%m/%d'),
        'filename': uuid.uuid4().hex,
        'ext': ext.lower(),
    }

    return 'uploads/{user_id}/{album_id}/{filename}{ext}'.format(**format_dict)


class Album(TimeStampedModel):
    """
    decimal  decimal     distance
    places   degrees    (in meters)
    -------  ---------  -----------
      1      0.1000000  11,057.43      11 km
      2      0.0100000   1,105.74       1 km
      3      0.0010000     110.57
      4      0.0001000      11.06
      5      0.0000100       1.11
      6      0.0000010       0.11      11 cm
      7      0.0000001       0.01       1 cm
    """

    user = models.ForeignKey(User, related_name='+')
    name = models.CharField(max_length=128)
    date = models.DateTimeField(default=datetime.utcnow)
    lng = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0'), validators=[MinValueValidator(Decimal('-180.0')), MaxValueValidator(Decimal('180.0'))])
    lat = models.DecimalField(max_digits=9, decimal_places=6, default=Decimal('0.0'), validators=[MinValueValidator(Decimal('-90.0')), MaxValueValidator(Decimal('90.0'))])

    def __str__(self):
        return '{} ({} - {})'.format(self.name, self.id, self.user, )

class JobStartFailedException(Exception):
    pass

class UploadedFile(TimeStampedModel):
    class Meta:
        permissions = (
            ("reanalyze_result", "Can submit UploadedFile for analysis"),
        )

    class Status:
        NEW = 'new'
        STAGE_1_STARTED = 'stage_1_started'
        STAGE_1_COMPLETE = 'stage_1_complete'
        STAGE_1_FAILED = 'stage_1_failed'
        STAGE_2_STARTED = 'stage_2_started'
        STAGE_2_COMPLETE = 'stage_2_complete'
        STAGE_2_FAILED = 'stage_2_failed'

        CHOICES = (
            (NEW, 'New upload'),
            (STAGE_1_STARTED, 'Stage 1 started'),
            (STAGE_1_COMPLETE, 'Stage 1 complete'),
            (STAGE_1_FAILED, 'Stage 1 failed'),
            (STAGE_2_STARTED, 'Stage 2 started'),
            (STAGE_2_COMPLETE, 'Stage 2 complete'),
            (STAGE_2_FAILED, 'Stage 2 failed')
        )

    file = models.FileField(upload_to=uploaded_file_to, max_length=255)
    thumbnail = models.FileField(upload_to=uploaded_file_to, max_length=255, null=True)
    thumbnail_labeled = models.FileField(upload_to=uploaded_file_to, max_length=255, null=True)

    album = models.ForeignKey(Album, related_name='uploads')
    original_filename = models.CharField(max_length=255, blank=True)
    filesize = models.BigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=30)

    status = models.CharField(choices=Status.CHOICES, default=Status.NEW, max_length=20)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()

        super(__class__, self).delete(using, keep_parents)

    def __str__(self):
        return '{} {}'.format(self.id, self.original_filename)

    def get_file_location(self, path):
        return 's3://{bucket}/{path}'.format(bucket=settings.AWS_STORAGE_BUCKET_NAME, path=path)

    def start_stage1(self):
        logger.info('Starting stage1 {}'.format(self.id))

        if settings.PROCESSING_PIPELINE == 'PROD':
            import boto3
            client = boto3.client('ecs')
            cluster = settings.ECS_CLUSTER_NAME
            task_family = 'image_preprocessor'

            result = client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
                'containerOverrides': [{
                    'name': 'image_preprocessor',
                    'command': [
                        self.get_file_location(self.file.name),
                        str(self.id)
                    ],
                }, ], }, )

            if 'failures' in result and len(result['failures']) > 0:
                msg = ", ".join(f['reason'] for f in result['failures'])
                logger.warning('Failed to start stage1 for {} due to {}'.format(self.id, msg))
                raise JobStartFailedException(msg)
            else:
                logger.info('Successfully started stage1 for {} '.format(self.id))
                self.status = UploadedFile.Status.STAGE_1_STARTED
                self.save()

        elif settings.PROCESSING_PIPELINE == 'LOCAL':
            raise NotImplemented("Needs to be implemented using local docker instance")

    def stage_1_completed(self):
        logger.info('stage1_completed {}'.format(self.id))

        path_with_basename, ext = splitext(self.file.name)

        self.status = UploadedFile.Status.STAGE_1_COMPLETE
        self.thumbnail.name = '{path}{ext}'.format(path=path_with_basename, ext='_preview.jpg')
        self.save()

    def stage_1_failed(self):
        logger.info('stage1_failed {}'.format(self.id))

        self.status = UploadedFile.Status.STAGE_1_FAILED
        self.save()

    def start_stage2(self):
        logger.info('starting stage2 {}'.format(self.id))

        if settings.PROCESSING_PIPELINE == 'PROD':
            import boto3
            client = boto3.client('ecs')
            cluster = settings.ECS_CLUSTER_NAME
            task_family = 'image_calibration'

            result = client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
                'containerOverrides': [{
                    'name': 'image_calibration',
                    'command': [
                        self.get_file_location(self.file.name),
                        str(self.id),
                        str(self.album.lng),
                        str(self.album.lat),
                        str(self.album.date),
                    ],
                }, ], }, )

            if 'failures' in result and len(result['failures']) > 0:
                msg = ", ".join(f['reason'] for f in result['failures'])
                logger.warning('Failed to start stage2 for {} due to {}'.format(self.id, msg))
                raise JobStartFailedException(msg)
            else:
                logger.info('Successfully started stage2 for {} '.format(self.id))
                self.status = UploadedFile.Status.STAGE_2_STARTED
                self.save()

        elif settings.PROCESSING_PIPELINE == 'LOCAL':
            raise NotImplemented("Needs to be implemented using local docker instance")

    def stage_2_completed(self):
        logger.info('stage2_completed {}'.format(self.id))

        path_with_basename, ext = splitext(self.file.name)

        self.status = UploadedFile.Status.STAGE_2_COMPLETE
        self.thumbnail_labeled.name = '{path}{ext}'.format(path=path_with_basename, ext='_labels.jpg')
        self.save()

    def stage_2_failed(self):
        logger.info('stage2_failed {}'.format(self.id))

        self.status = UploadedFile.Status.STAGE_2_FAILED
        self.save()
