import logging

from django.core.management.base import BaseCommand
from django.db import transaction

from reefsource.apps.operations.tasks import process_recurring_operations
from reefsource.apps.securities.tasks import collect_symbol_close_prices

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates everything that is required for this project to work'

    def handle(self, *args, **options):
        logger.info('setup defaults complete')
