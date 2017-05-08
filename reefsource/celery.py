from __future__ import absolute_import

import celery
import os
import raven
from django.conf import settings
from raven.contrib.celery import register_signal, register_logger_signal

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reefsource.settings.local')


class Celery(celery.Celery):
    def on_configure(self):
        client = raven.Client(settings.RAVEN_CONFIG.get('dsn', ''))

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


app = Celery('reefsource')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
