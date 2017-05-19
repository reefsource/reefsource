from rest_framework import generics
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from reefsource.apps.albums.models import UploadedFile, Album, Result
from .serializers import UploadedFileSerializer, AlbumSerializer, ResultSerializer, AlbumDetailSerializer


class FileUpload(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        queryset = super(FileUpload, self).get_queryset()
        queryset = queryset.filter(album=self.request.user)

        return queryset

    def perform_create(self, serializer):
        params = {'album': self.request.user,
                  'original_filename': serializer.validated_data['file'].name,
                  'filesize': serializer.validated_data['file'].size,
                  'mime_type': serializer.validated_data['file'].content_type}

        serializer.save(**params)


class FileUploadView(APIView):
    parser_classes = (FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        # ...
        # do some stuff with uploaded file
        # ...
        return Response(status=204)


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
