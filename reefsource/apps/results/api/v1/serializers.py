from reefsource.apps.results.models import Result
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class ResultSerializer(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = '__all__'
        read_only_fields = ('id', 'created', 'modified', 'json')
