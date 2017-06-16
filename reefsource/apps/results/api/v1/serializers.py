from rest_framework import serializers

from reefsource.apps.results.models import Result
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer
from reefsource.core.rest_framework.validators import NonBlankValidator


class AnalysisResultSerializer(serializers.Serializer):
    score = serializers.DecimalField(max_digits=16, decimal_places=12)


class Stage2ResultSerializer(serializers.Serializer):
    GPSLongitude = serializers.FloatField(max_value=180, min_value=-180)
    GPSLatitude = serializers.FloatField(max_value=90, min_value=-90)
    coral = AnalysisResultSerializer()


class ResultSerializer(AppendIdModelSerializer):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.fields['uploaded_file_id'].validators = []

    class Meta:
        model = Result
        fields = ('id', 'created', 'modified', 'uploaded_file', 'stage', 'json',)
        extra_kwargs = {'json': {'validators': [NonBlankValidator()]}}
        read_only_fields = ('id', 'created', 'modified',)


class ResultSerializerForMap(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = ('uploaded_file', 'modified', 'location', 'score',)
