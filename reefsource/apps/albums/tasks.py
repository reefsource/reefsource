import logging

import random
from celery import shared_task

from reefsource.apps.albums.models import UploadedFile

logger = logging.getLogger(__name__)


@shared_task(max_retries=None, rate_limit='3/m')
def stage1(upload_id):
    try:
        UploadedFile.objects.get(pk=upload_id).start_stage1()
    except Exception as e:
        stage1.retry(countdown=60 * 3 + random.randint(-60, 60), exc=e)


@shared_task(max_retries=None, rate_limit='3/m')
def stage2(upload_id):
    try:
        UploadedFile.objects.get(pk=upload_id).start_stage2()
    except Exception as e:
        stage2.retry(countdown=60 * 3 + random.randint(-60, 60), exc=e)
