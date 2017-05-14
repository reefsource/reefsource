from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions

from reefsource.apps.albums.models import  UploadedFile
from .serializers import  UploadedFileSerializer


class FileUpload(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        queryset = super(FileUpload, self).get_queryset()
        queryset = queryset.filter(user_id=self.request.user)

        return queryset

    def perform_create(self, serializer):
        params = {'user_id': self.request.user,
                  'original_filename': serializer.validated_data['file'].name,
                  'filesize': serializer.validated_data['file'].size,
                  'mime_type': serializer.validated_data['file'].content_type}

        serializer.save(**params)
