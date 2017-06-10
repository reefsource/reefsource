import json

from rest_framework.relations import ManyRelatedField, PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SlugRelatedField, Field


class IdManyRelatedField(ManyRelatedField):
    field_name_suffix = '_ids'

    def bind(self, field_name, parent):
        self.source = field_name[:-len(self.field_name_suffix)]
        super(IdManyRelatedField, self).bind(field_name, parent)


class IdPrimaryKeyRelatedField(PrimaryKeyRelatedField):
    """
    Field that  the field name to FIELD_NAME_id.
    Only works together the our ModelSerializer.
    """
    many_related_field_class = IdManyRelatedField
    field_name_suffix = '_id'

    def bind(self, field_name, parent):
        """
        Called when the field is bound to the serializer.
        Changes the source  so that the original field name is used (removes
        the _id suffix).
        """
        if field_name:
            self.source = field_name[:-len(self.field_name_suffix)]
        super(IdPrimaryKeyRelatedField, self).bind(field_name, parent)


class AppendIdModelSerializer(ModelSerializer):
    '''
    Append '_id' to FK field names
    https://gist.github.com/ostcar/eb78515a41ab41d1755b
    '''
    serializer_related_field = IdPrimaryKeyRelatedField

    def get_fields(self):
        fields = super(AppendIdModelSerializer, self).get_fields()
        new_fields = type(fields)()
        for field_name, field in fields.items():
            if getattr(field, 'field_name_suffix', None):
                field_name += field.field_name_suffix
            new_fields[field_name] = field
        return new_fields


class CreatableSlugRelatedField(SlugRelatedField):
    def __init__(self, slug_field=None, **kwargs):
        self.context = kwargs.pop('context', {})
        super(CreatableSlugRelatedField, self).__init__(slug_field, **kwargs)

    def to_internal_value(self, data):
        try:
            tmp = self.context.copy()
            tmp.update(**{self.slug_field: data})  # which returns None since it mutates z

            return self.get_queryset().get_or_create(**tmp)[0]
        except (TypeError, ValueError):
            self.fail('invalid')


class JSONField(Field):
    def to_representation(self, obj):
        return json.loads(obj)

    def to_internal_value(self, data):
        return json.dumps(data)
