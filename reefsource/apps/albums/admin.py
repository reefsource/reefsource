from django.contrib import admin
from django_admin_listfilter_dropdown.filters import DropdownFilter, RelatedDropdownFilter

# Register your models here.
from reefsource.apps.albums.tasks import stage1, stage2
from .models import UploadedFile, Album


def my_delete_selected(modeladmin, request, queryset):
    for obj in queryset:
        obj.delete()


my_delete_selected.short_description = "Deletes selected files"


def start_stage1(modeladmin, request, queryset):
    for obj in queryset:
        stage1.delay(obj.id)


start_stage1.short_description = "Force start stage 1"


def start_stage2(modeladmin, request, queryset):
    for obj in queryset:
        stage2.delay(obj.id)


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

    list_filter = ('status',
                   ('album__user', RelatedDropdownFilter),
                   ('album', RelatedDropdownFilter),
                   )
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
        'name',
        'user',
        'uploaded_file_count',
        'lat',
        'lng',
    )
    list_filter = ('user',)
    readonly_fields = (
        'created',
        'modified')

    def uploaded_file_count(self, obj):
        return obj.uploads.count()

    uploaded_file_count.short_description = "# of images"
