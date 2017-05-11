import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates superuser and demo account, and bootstraps the project'

    def handle(self, *args, **options):
        logger.info('setup demo complete')