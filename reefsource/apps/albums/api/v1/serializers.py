from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from reefsource.apps.albums.models import UploadedFile, Album
from reefsource.apps.results.api.v1.serializers import ResultSerializer, ResultSerializerForAlbum
from reefsource.core.rest_framework.serializers import AppendIdModelSerializer


class UploadedFileSerializer(AppendIdModelSerializer):
    result = ResultSerializer(read_only=True)

    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('original_filename', 'filesize', 'uploaded_by', 'mime_type', 'album', 'thumbnail', 'thumbnail_labeled', 'status', 'result')


class EmptyUploadedFileSerializer(ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ('id', 'status', 'modified',)
        read_only_fields = ('id', 'status', 'modified',)


class AlbumSerializer(AppendIdModelSerializer):
    upload_count = SerializerMethodField()

    class Meta:
        model = Album
        fields = ('id', 'created', 'modified', 'name', 'lat', 'lng', 'date', 'upload_count')
        read_only_fields = ('id', 'created', 'modified', 'upload_count')

    def get_upload_count(self, obj):
        return obj.uploads.count()


class UploadedFileSerializerForAlbum(AppendIdModelSerializer):
    result = ResultSerializerForAlbum(read_only=True)

    class Meta:
        model = UploadedFile
        fields = '__all__'
        read_only_fields = ('original_filename', 'filesize', 'uploaded_by', 'mime_type', 'album', 'thumbnail', 'thumbnail_labeled', 'status', 'result')


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

        return UploadedFileSerializerForAlbum(uploads, many=True).data
