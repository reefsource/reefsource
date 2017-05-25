import logging
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, UserManager

logger = logging.getLogger(__name__)


class AppUserManager(UserManager):
    pass


class User(AbstractUser):
    objects = AppUserManager()

    def __str__(self):
        return '{}'.format(self.email)

    @transaction.atomic
    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)