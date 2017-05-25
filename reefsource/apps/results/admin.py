from django.contrib import admin

from .models import Result


@admin.register(Result)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = (
        'uploaded_file',
        'stage',
        'json'
    )
