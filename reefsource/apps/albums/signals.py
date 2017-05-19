from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from reefsource.apps.albums.models import Album


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Album.objects.create(user=instance, name='Default Album')
