from rest_framework import generics
from rest_framework.permissions import AllowAny

from reefsource.apps.albums.models import UploadedFile, Album, Result
from .serializers import UploadedFileSerializer, AlbumSerializer, ResultSerializer


class FileUpload(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    # def get_queryset(self):
    #     queryset = super(FileUpload, self).get_queryset()
    #     queryset = queryset.filter(album=self.request.user)
    #
    #     return queryset

    # def perform_create(self, serializer):
    #     params = {'user': self.request.user,
    #               'original_filename': serializer.validated_data['file'].name,
    #               'filesize': serializer.validated_data['file'].size,
    #               'mime_type': serializer.validated_data['file'].content_type}
    #
    #     serializer.save(**params)


class AlbumApiMixin(object):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = super(AlbumApiMixin, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class AlbumList(AlbumApiMixin, generics.ListCreateAPIView):
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumDetail(AlbumApiMixin, generics.RetrieveUpdateDestroyAPIView):
    pass


class ResultList(generics.ListAPIView):
    permission_classes = (AllowAny, )
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
