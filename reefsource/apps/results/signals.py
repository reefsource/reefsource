import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from reefsource.apps.albums.tasks import stage2
from reefsource.apps.results.models import Result

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Result)
def process_stage1_result(sender, instance: Result = None, created=False, **kwargs):
    if created and instance.stage == Result.Stage.STAGE_1:
        logger.info('scheduling start of stage 2 {}'.format(instance.id))
        stage2.delay(instance.uploaded_file.id)
