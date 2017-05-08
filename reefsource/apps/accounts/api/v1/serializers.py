import six
from rest_framework import serializers

from reefsource.apps.accounts.models import UploadedFile
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class UploadedFileSerializer(AppendIdModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('app_account', 'original_filename', 'filesize', 'uploaded_by', 'mime_type')
