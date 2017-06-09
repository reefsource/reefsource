from reefsource.apps.results.models import Result
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class ResultSerializer(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = ('id', 'created', 'modified', 'uploaded_file', 'json', 'stage', 'lat', 'lng', 'score')
        read_only_fields = ('id', 'created', 'modified', 'json', 'stage', 'lat', 'lng', 'score')


class SimpleResultSerializer(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = 'created', 'lat', 'lng', 'score', 'uploaded_file'
