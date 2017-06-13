from django.contrib.gis.db.models import PointField
from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils.models import TimeStampedModel

from reefsource.apps.albums.models import UploadedFile


class Result(TimeStampedModel):
    class Stage:
        STAGE_1 = 'stage_1'
        STAGE_2 = 'stage_2'

        CHOICES = (
            (STAGE_1, 'Stage 1'),
            (STAGE_2, 'Stage 2')
        )

    uploaded_file = models.OneToOneField(UploadedFile, related_name='result')

    stage = models.CharField(choices=Stage.CHOICES, max_length=20)
    success = models.BooleanField()
    json = JSONField()

    location = PointField(null=True)
    score = models.DecimalField(max_digits=9, decimal_places=6, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.id, self.uploaded_file.id, self.stage)
