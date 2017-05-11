import logging

from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Creates everything that is required for this project to work'

    def handle(self, *args, **options):
        logger.info('setup defaults complete')
