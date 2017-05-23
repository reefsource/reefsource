import logging
import uuid

from django.conf import settings
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
    user = models.ForeignKey(User, related_name='+')
    name = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)


class UploadedFile(TimeStampedModel):
    class Status(object):
        NEW = 'new'
        STAGE_1_STARTED = 'stage_1_started'
        STAGE_1_COMPLETE = 'stage_1_complete'
        STAGE_2_STARTED = 'stage_2_started'
        STAGE_2_COMPLETE = 'stage_2_complete'

        CHOICES = (
            (NEW, 'New upload'),
            (STAGE_1_STARTED, 'Stage 1 started'),
            (STAGE_1_COMPLETE, 'Stage 1 complete'),
            (STAGE_2_STARTED, 'Stage 2 started'),
            (STAGE_2_COMPLETE, 'Stage 2 complete')
        )

    file = models.FileField(upload_to=uploaded_file_to, max_length=255)
    thumbnail = models.FileField(upload_to=uploaded_file_to, max_length=255, null=True)

    album = models.ForeignKey(Album, related_name='uploads')
    original_filename = models.CharField(max_length=255, blank=True)
    filesize = models.BigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=30)

    status = models.CharField(choices=Status.CHOICES, default=Status.NEW, max_length=20)

    @classmethod
    def set_status(cls, upload_id, status):
        upload = UploadedFile.objects.get(pk=upload_id)
        upload.status = status

        if (status == UploadedFile.Status.STAGE_1_COMPLETE):
            upload.thumbnail.name = splitext(upload.file.name)[0] + '_preview.jpg'

        upload.save()

    @classmethod
    def get_file_location(cls, path):
        return 's3://{bucket}/{path}'.format(bucket=settings.AWS_STORAGE_BUCKET_NAME, path=path)

    @classmethod
    def stage1(cls, upload_id, path):
        logger.info('starting stage1')

        import boto3
        client = boto3.client('ecs')
        cluster = 'reefsource'
        task_family = 'image_preprocessor'

        client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
            'containerOverrides': [{
                'name': 'image_preprocessor',
                'command': [
                    cls.get_file_location(path),
                    str(upload_id),
                ],
            }, ], }, )

        UploadedFile.set_status(upload_id, UploadedFile.Status.STAGE_1_STARTED)

    @classmethod
    def stage2(cls, upload_id, path):
        logger.info('starting stage2')

        import boto3
        client = boto3.client('ecs')
        cluster = 'reefsource'
        task_family = 'image_calibration'

        client.run_task(cluster=cluster, taskDefinition='{}'.format(task_family), overrides={
            'containerOverrides': [{
                'name': 'image_calibration',
                'command': [
                    cls.get_file_location(path),
                    str(upload_id),
                ],
            }, ], }, )

        UploadedFile.set_status(upload_id, UploadedFile.Status.STAGE_2_STARTED)
