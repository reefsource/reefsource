import logging

from celery import shared_task

from reefsource.apps.albums.models import UploadedFile

logger = logging.getLogger(__name__)


@shared_task
def stage1(upload_id, path):
    UploadedFile.stage1(upload_id, path)

@shared_task
def stage2(upload_id, path):
    UploadedFile.stage2(upload_id, path)
