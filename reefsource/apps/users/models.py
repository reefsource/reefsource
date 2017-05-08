from __future__ import unicode_literals

import logging

from django.contrib.auth.models import AbstractUser, UserManager

logger = logging.getLogger(__name__)


class AppUserManager(UserManager):
    pass


class User(AbstractUser):
    objects = AppUserManager()

    def __unicode__(self):
        return '{} {}'.format(self.first_name, self.last_name)
