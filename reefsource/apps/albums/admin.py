from django.contrib import admin

# Register your models here.
from .models import UploadedFile, Album


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('album', 'original_filename', 'file', 'filesize', 'mime_type')


@admin.register(Album)
class AlbumsAdmin(admin.ModelAdmin):
    list_display = (
    'id',
    'created',
    'modified',
    'user',
    'name',
    'lat',
    'long',
    )
