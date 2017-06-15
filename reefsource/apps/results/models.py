import json

from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
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
    score = models.DecimalField(max_digits=16, decimal_places=12, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.id, self.uploaded_file.id, self.stage)

    @classmethod
    def process(cls, uploaded_file, stage, result_json_str):

        is_valid = None
        results = {}

        result = json.loads(result_json_str)

        if stage == Result.Stage.STAGE_1:
            is_valid = 'error' not in result

        elif stage == Result.Stage.STAGE_2:
            from reefsource.apps.results.api.v1.serializers import Stage2ResultSerializer
            stage2_result = Stage2ResultSerializer(data=result)

            is_valid = stage2_result.is_valid()

            if is_valid:
                results['location'] = Point(x=stage2_result.validated_data['GPSLongitude'], y=stage2_result.validated_data['GPSLatitude'], srid=4326)
                results['score'] = stage2_result.validated_data['coral']['score']

        Result.objects.update_or_create(uploaded_file=uploaded_file, defaults={**{
            'stage': stage,
            'success': is_valid,
            'json': result_json_str
        }, **results})

        return is_valid
