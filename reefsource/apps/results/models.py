from django.db import models

# Create your models here.
from model_utils.models import TimeStampedModel

from reefsource.apps.albums.models import UploadedFile


class Result(TimeStampedModel):
    uploaded_file = models.ForeignKey(UploadedFile)
    json = models.TextField()