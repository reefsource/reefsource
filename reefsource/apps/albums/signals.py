import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from reefsource.apps.albums.models import UploadedFile
from reefsource.apps.albums.tasks import stage1

logger = logging.getLogger(__name__)


@receiver(post_save, sender=UploadedFile)
def process_upload(sender, instance: UploadedFile = None, created=False, **kwargs):
    if created:
        logger.info('scheduling start of stage 1 {}'.format(instance))
        stage1.delay(instance.id)
