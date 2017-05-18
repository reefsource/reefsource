import logging
import random

from django.core.management.base import BaseCommand

from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates made up data'

    def add_arguments(self, parser):
        parser.add_argument('-u', '--users', required=False, type=int, default=10, help='Creates n users')
        parser.add_argument('--all', action='store_true', required=False, help='Creates all types of objects')

        parser.add_argument('--app_account_id', required=False, type=int, help='Creates objects under the specified app account id')

    def handle(self, *args, **options):
        if options['all'] or options['users']:
            self.create_users(options['users'], options['app_account_id'])

    def create_users(self, number_of_users, app_account_id=None):
        word_list = self.get_word_list()

        for i in range(0, number_of_users):
            user = User()
            user.first_name = random.choice(word_list).title()
            user.last_name = random.choice(word_list).title()
            user.username = ('%s_%s' % (user.first_name, user.last_name)).lower()
            user.email = '%s@demo.com' % (user.username,)
            user.set_password('%s123' % user.username)
            user.save()

    def get_word_list(self):
        from django.core.cache import cache

        key = 'backfill:words'

        word_list = cache.get(key)
        if not word_list:
            import requests
            word_list_url = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
            response = requests.get(word_list_url)
            word_list = response.content.splitlines()
            cache.set(key, word_list)

        return word_list
