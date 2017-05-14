import six
from rest_framework import serializers

from reefsource.apps.albums.models import UploadedFile
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class UploadedFileSerializer(AppendIdModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('original_filename', 'filesize', 'uploaded_by', 'mime_type')
