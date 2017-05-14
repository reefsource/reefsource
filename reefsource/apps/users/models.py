import logging

from django.contrib.auth.models import AbstractUser, UserManager

logger = logging.getLogger(__name__)


class AppUserManager(UserManager):
    pass


class User(AbstractUser):
    objects = AppUserManager()

    def __unicode__(self):
        return '{}'.format(self.email)
