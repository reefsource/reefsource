from __future__ import unicode_literals

from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'reefsource.apps.users'

    def ready(self):
        import reefsource.apps.users.signals