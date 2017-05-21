from rest_framework import generics
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny

from reefsource.apps.albums.models import UploadedFile, Album, Result
from .serializers import UploadedFileSerializer, AlbumSerializer, ResultSerializer, AlbumDetailSerializer


class FileUploadView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser,)

    def __init__(self):
        super(FileUploadView, self).__init__()
        self.albumId = None

    def get_queryset(self):
        queryset = super(FileUploadView, self).get_queryset()
        queryset = queryset.filter(album__user=self.request.user)

        return queryset

    def create(self, request, albumId, *args, **kwargs):
        self.albumId = albumId
        return super(FileUploadView, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        params = {'album_id': self.albumId,
                  'original_filename': serializer.validated_data['file'].name,
                  'filesize': serializer.validated_data['file'].size,
                  'mime_type': serializer.validated_data['file'].content_type}

        serializer.save(**params)


class AlbumApiMixin(object):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = super(AlbumApiMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class AlbumListView(AlbumApiMixin, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumDetailView(AlbumApiMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumDetailSerializer


class ResultListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
