from django.conf import settings
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from reefsource.apps.users.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance: User = None, created=False, **kwargs):
    if created:
        group = Group.objects.get(name='regular users')
        instance.groups.add(group)

        Token.objects.create(user=instance)
