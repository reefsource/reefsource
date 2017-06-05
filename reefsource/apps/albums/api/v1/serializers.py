from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from reefsource.apps.albums.models import UploadedFile, Album
from reefsource.apps.results.api.v1.serializers import ResultSerializer
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class UploadedFileSerializer(AppendIdModelSerializer):
    results = ResultSerializer(many=True)
    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('original_filename', 'filesize', 'uploaded_by', 'mime_type', 'album', 'thumbnail', 'thumbnail_labeled', 'status' , 'results')


class AlbumSerializer(AppendIdModelSerializer):
    upload_count = SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'created', 'modified', 'name', 'lat', 'lng', 'upload_count')
        read_only_fields = ('id', 'created', 'modified', 'upload_count')

    def get_upload_count(self, obj):
        return obj.uploads.count()


class AlbumDetailSerializer(AppendIdModelSerializer):
    uploads = serializers.SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'created', 'modified', 'name', 'date', 'lat', 'lng', 'uploads')
        read_only_fields = ('id', 'created', 'modified', 'upload_count', 'uploads')

    def get_uploads(self, instance):
        uploads = UploadedFile.objects \
            .filter(album_id=instance.id) \
            .order_by('created')

        return UploadedFileSerializer(uploads, many=True).data
