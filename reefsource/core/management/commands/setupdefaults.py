import logging

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates everything that is required for this project to work'

    def handle(self, *args, **options):
        with transaction.atomic():

            logger.info('setting up default users')
            User.objects.update_or_create(username='lkarolewski', defaults={
                'is_superuser': True,
                'is_staff': True
            })

            logger.info('setting up defaults groups')
            user_group, created = Group.objects.get_or_create(name="regular users")
            user_group.permissions.clear()

            for perm in self._get_permissions([
                'users.change_user',

                'albums.add_album',
                'albums.change_album',
                'albums.delete_album',

                'albums.add_uploadedfile'
            ]):
                user_group.permissions.add(perm)

            user_group.save()

            for user in User.objects.all():
                user.groups.add(user_group)

            logger.info('setup defaults complete')

    def _get_permissions(self, permission_names):
        """
        Fetches the permission objects from config markup
        """
        permissions = []
        for perm in permission_names:

            try:
                app_label, codename = perm.split('.', 1)
            except IndexError:
                raise AttributeError(
                    "The format of identifier string permission (perm) is wrong. "
                    "It should be in 'app_label.codename'."
                )

            try:
                permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
            except Permission.DoesNotExist as e:
                self.stderr.write("Error: Permission %s does not exist" % perm)
            else:
                permissions.append(permission)

        return permissions
