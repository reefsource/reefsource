from reefsource.settings.base import *

INTERNAL_IPS = (
    '127.0.0.1',
    '10.0.2.2',
)

if not DEBUG:
    STATIC_URL = '/nginx/static/'
    MEDIA_URL = '/nginx/media/'