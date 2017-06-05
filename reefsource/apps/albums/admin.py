from django.contrib import admin

# Register your models here.
from .models import UploadedFile, Album


def my_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


my_delete_selected.short_description = "Deletes selected files"


def start_stage1(modeladmin, request, queryset):
    for obj in queryset:
        obj.start_stage1()


start_stage1.short_description = "Force start stage 1"


def start_stage2(modeladmin, request, queryset):
    for obj in queryset:
        obj.start_stage2()


start_stage2.short_description = "Force start stage 2"


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ('album',
                    'created',
                    'modified',
                    'status',
                    'original_filename',
                    'file',
                    'filesize')
    readonly_fields = (
        'created',
        'modified')

    actions = [my_delete_selected, start_stage1, start_stage2]

    def get_actions(self, request):
        actions = super(__class__, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


@admin.register(Album)
class AlbumsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'user',
        'name',
        'lat',
        'lng',
    )
    readonly_fields = (
        'created',
        'modified')
