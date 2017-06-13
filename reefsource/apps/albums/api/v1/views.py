from rest_framework import filters, status
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from reefsource.apps.albums.models import UploadedFile, Album
from reefsource.core.rest_framework.permissions import CustomPermission
from .serializers import UploadedFileSerializer, AlbumSerializer, AlbumDetailSerializer, EmptyUploadedFileSerializer


class FileUploadView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    parser_classes = (MultiPartParser,)

    def __init__(self):
        super(__class__, self).__init__()
        self.albumId = None

    def get_queryset(self):
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(album__user=self.request.user)

        return queryset

    def create(self, request, albumId, *args, **kwargs):
        self.albumId = albumId
        return super(__class__, self).create(request, *args, **kwargs)

    def perform_create(self, serializer):
        params = {'album_id': self.albumId,
                  'original_filename': serializer.validated_data['file'].name,
                  'filesize': serializer.validated_data['file'].size,
                  'mime_type': serializer.validated_data['file'].content_type}

        serializer.save(**params)


class FileUploadViewDetailView(generics.RetrieveDestroyAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(album__user=self.request.user)

        return queryset


class FileUploadReanalyzePermission(CustomPermission):
    required_perms = ('reanalyze_result',)


class FileUploadReanalyzeView(GenericAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = EmptyUploadedFileSerializer
    permission_classes = (FileUploadReanalyzePermission,)

    def post(self, request, *args, **kwargs):
        instance = self.get_object()

        from reefsource.apps.results.models import Result
        Result.objects.filter(uploaded_file=instance).delete()

        instance.start_stage1()

        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AlbumApiMixin(object):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

    def get_queryset(self):
        queryset = super(__class__, self).get_queryset()
        queryset = queryset.filter(user=self.request.user)

        return queryset


class AlbumListView(AlbumApiMixin, generics.ListCreateAPIView):
    filter_backends = (filters.OrderingFilter, filters.SearchFilter,)
    ordering_fields = ('name', 'created', 'modified', 'date',)
    ordering = ('-date',)
    search_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AlbumDetailView(AlbumApiMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlbumDetailSerializer
