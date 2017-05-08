"""
WSGI config for reefsource project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os
from dj_static import Cling, MediaCling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reefsource.settings.local")

application = Cling(MediaCling(get_wsgi_application()))
