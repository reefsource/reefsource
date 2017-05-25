from django.contrib.postgres.fields import JSONField
from django.db import models
from model_utils.models import TimeStampedModel

from reefsource.apps.albums.models import UploadedFile


class Result(TimeStampedModel):
    class Meta:
        unique_together = (("uploaded_file", "stage"),)
        permissions = (
            ("add_stage1_result", "Can add result for stage 1"),
            ("add_stage2_result", "Can add result for stage 2"),
        )

    class Stage:
        STAGE_1 = 'stage_1'
        STAGE_2 = 'stage_2'

        CHOICES = (
            (STAGE_1, 'Stage 1'),
            (STAGE_2, 'Stage 2')
        )

    uploaded_file = models.ForeignKey(UploadedFile)
    stage = models.CharField(choices=Stage.CHOICES, default=Stage.STAGE_1, max_length=20)
    json = JSONField()

    def __str__(self):
        return '{} {} {}'.format(self.id, self.uploaded_file.id, self.stage)
