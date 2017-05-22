import uuid

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

from reefsource.apps.users.models import User


def uploaded_file_to(instance, filename):
    """
    Determine where the uploaded file should go on the server.
    """
    filename = filename.split('/')[-1]

    try:
        ext = '.' + filename.split('.')[-1]
    except IndexError:
        ext = ''

    format_dict = {
        'user_id': instance.album.user.id,
        'album_id': instance.album.id,
        'date': timezone.now().strftime('%Y/%m/%d'),
        'filename': uuid.uuid4().hex,
        'ext': ext.lower(),
    }

    return 'uploads/{user_id}/{album_id}/{filename}{ext}'.format(**format_dict)


class Album(TimeStampedModel):
    user = models.ForeignKey(User, related_name='+')
    name = models.CharField(max_length=128)
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True)
    long = models.DecimalField(max_digits=9, decimal_places=6, null=True)


class UploadedFile(TimeStampedModel):
    file = models.FileField(upload_to=uploaded_file_to, max_length=255)
    thumbnail = models.CharField(null=True, max_length=255)

    album = models.ForeignKey(Album, related_name='uploads')
    original_filename = models.CharField(max_length=255, blank=True)
    filesize = models.BigIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=30)
