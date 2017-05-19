from django.apps import AppConfig


class AlbumsConfig(AppConfig):
    name = 'reefsource.apps.albums'

    def ready(self):
        import reefsource.apps.albums.signals