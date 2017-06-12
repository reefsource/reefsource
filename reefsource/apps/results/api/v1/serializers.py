from reefsource.apps.results.models import Result

from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class ResultSerializer(AppendIdModelSerializer):
    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self.fields['uploaded_file_id'].validators = []

    class Meta:
        model = Result
        fields = ('id', 'created', 'modified', 'uploaded_file', 'stage', 'json',)
        read_only_fields = ('id', 'created', 'modified',)

    def validate_uploaded_file(self):
        return True


class ResultSerializerForMap(AppendIdModelSerializer):
    class Meta:
        model = Result
        fields = ('uploaded_file', 'modified', 'location', 'score',)
