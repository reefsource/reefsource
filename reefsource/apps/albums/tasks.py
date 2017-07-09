import logging

import random
from celery import shared_task

from reefsource.apps.albums.models import UploadedFile, JobStartFailedException

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=None, rate_limit='3/m')
def stage1(self, upload_id):
    try:
        logger.info('Picked up job to start stage1 for {}, attempt {}'.format(upload_id, stage1.request.retries))
        UploadedFile.objects.get(pk=upload_id).start_stage1()

    except JobStartFailedException as e:
        countdown = 60 * self.request.retries + random.randint(0, 60)
        logger.info('Retrying stage1 for {} in {}'.format(upload_id, countdown))
        self.retry(countdown=countdown, exc=e)

    except Exception as e:
        countdown = 60 * self.request.retries + random.randint(0, 60)
        logger.exception('Retrying stage1 for {} in {}s'.format(upload_id, countdown))
        self.retry(countdown=countdown, exc=e)


@shared_task(bind=True, max_retries=None, rate_limit='3/m')
def stage2(self, upload_id):
    try:
        logger.info('Picked up job to start stage2 for {}, attempt {}'.format(upload_id, stage2.request.retries))
        UploadedFile.objects.get(pk=upload_id).start_stage2()

    except JobStartFailedException as e:
        countdown = 60 * self.request.retries + random.randint(0, 60)
        logger.info('Retrying stage2 for {} in {}'.format(upload_id, countdown))
        self.retry(countdown=countdown, exc=e)

    except Exception as e:
        countdown = 60 * self.request.retries + random.randint(0, 60)
        logger.exception('Retrying stage2 for {} in {}'.format(upload_id, countdown))
        self.retry(countdown=countdown, exc=e)
