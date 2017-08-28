from django.contrib import admin

from reefsource.core.admin import SecureOSM
from .models import Result


@admin.register(Result)
class UploadedFileAdmin(SecureOSM):
    list_display = (
        'uploaded_file',
        'stage',
        'modified',
        'json',
    )
    list_filter = ('stage',)
    readonly_fields = (
        'created',
        'modified')
