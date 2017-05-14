from django.contrib import admin

# Register your models here.
from .models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'file', 'filesize', 'mime_type')
