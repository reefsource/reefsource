from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions

from reefsource.apps.accounts.models import  UploadedFile
from .serializers import  UploadedFileSerializer


class FileUpload(generics.ListCreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer

    def get_queryset(self):
        queryset = super(FileUpload, self).get_queryset()
        queryset = queryset.filter(app_account_id=self.request.user.app_account_id, uploaded_by=self.request.user)

        return queryset

    def perform_create(self, serializer):
        params = {'app_account_id': self.request.user.app_account_id,
                  'original_filename': serializer.validated_data['file'].name,
                  'filesize': serializer.validated_data['file'].size,
                  'uploaded_by': self.request.user,
                  'mime_type': serializer.validated_data['file'].content_type}

        serializer.save(**params)
