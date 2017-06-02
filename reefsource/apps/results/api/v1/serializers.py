from reefsource.apps.results.models import Result
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class ResultSerializer(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = 'id', 'created', 'modified', 'json', 'lat', 'lng', 'score'
        read_only_fields = ('id', 'created', 'modified', 'json', 'lat', 'lng', 'score')
