import os

os.environ.setdefault('DJANGO_DEBUG', 'False')

from .base import *

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

BROKER_BACKEND = 'memory'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    }
}

if os.getenv('CIRCLECI'):
    TEST_REPORT_DIR = os.getenv('CIRCLE_TEST_REPORTS', '~')
    TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
    TEST_OUTPUT_DIR = TEST_REPORT_DIR + '/django/'
    LOGGING['handlers']['console']['level'] = 'ERROR'

# LOGGING['loggers']['django.db.backends']['level'] = 'DEBUG'