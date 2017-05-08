from django.conf import settings

import reefsource


def version(request):
    return {
        'version': reefsource.__version__,
        'raven_dsn' :  settings.RAVEN_FRONTEND_CONFIG.get('dsn', ''),
        'inactivity_logout' : settings.SESSION_COOKIE_AGE
    }