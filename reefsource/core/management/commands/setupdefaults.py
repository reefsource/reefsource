import logging

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction
from rest_framework.authtoken.models import Token

from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Creates everything that is required for this project to work'

    def handle(self, *args, **options):
        with transaction.atomic():
            logger.info('setting up defaults groups')
            users_group, created = Group.objects.get_or_create(name="regular users")
            users_group.permissions.clear()

            self.assign_group_permissions(users_group, [
                'users.change_user',

                'albums.add_album',
                'albums.change_album',
                'albums.delete_album',

                'albums.add_uploadedfile'
            ])

            logger.info('setting up system user')
            system_user, created = User.objects.update_or_create(username='system')
            self.assign_user_permissions(system_user, [
                'results.add_result'
            ])
            Token.objects.get_or_create(user=system_user)

            logger.info('setting up admin user')
            User.objects.update_or_create(username='lkarolewski', defaults={
                'is_superuser': True,
                'is_staff': True
            })

            logger.info('setup defaults complete')

    def assign_user_permissions(self, user, permissions):
        for perm in self._get_permissions(permissions):
            user.user_permissions.add(perm)

    def assign_group_permissions(self, group, permissions):
        for perm in self._get_permissions(permissions):
            group.permissions.add(perm)

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
