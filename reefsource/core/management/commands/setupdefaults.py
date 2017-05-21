import logging

from django.core.management.base import BaseCommand

from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates everything that is required for this project to work'

    def handle(self, *args, **options):
        User.objects.update_or_create(username='lkarolewski', defaults={
            'is_superuser': True,
            'is_staff': True
        })

        logger.info('setup defaults complete')
