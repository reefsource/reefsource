import json

from rest_framework.serializers import Field


class JSONSerializerField(Field):
    def to_representation(self, obj):
        return json.loads(obj)

    def to_internal_value(self, data):
        return json.dumps(data)
