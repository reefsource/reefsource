from django.apps import AppConfig


class ResultsConfig(AppConfig):
    name = 'reefsource.apps.results'

    def ready(self):
        import reefsource.apps.results.signals