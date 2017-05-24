import logging

from celery import shared_task

from reefsource.apps.albums.models import UploadedFile

logger = logging.getLogger(__name__)


@shared_task
def stage1(upload_id):
    UploadedFile.objects.get(pk=upload_id).start_stage1()


@shared_task
def stage2(upload_id):
    UploadedFile.objects.get(pk=upload_id).start_stage2()
