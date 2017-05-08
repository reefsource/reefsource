from __future__ import unicode_literals

import logging
import uuid

from django.db import models
from django.utils import timezone
from model_utils.models import TimeStampedModel

logger = logging.getLogger(__name__)


# TODO move to UploadedFile
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
    'user_id': instance.uploaded_by_id,
    'date': timezone.now().strftime('%Y/%m/%d'),
    'filename': uuid.uuid4().hex,
    'ext': ext.lower(),
  }

  return 'accounts/{account_id}/files/{user_id}/{date}/{filename}{ext}'.format(**format_dict)


class UploadedFile(TimeStampedModel):
  original_filename = models.CharField(max_length=255, blank=True)
  file = models.FileField(upload_to=uploaded_file_to, max_length=255)
  filesize = models.BigIntegerField(blank=True, null=True)
  uploaded_by = models.ForeignKey('users.User')
  mime_type = models.CharField(max_length=30)
