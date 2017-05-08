from __future__ import absolute_import

from .celery import app as celery_app
from .version import build, githash

major = 1
minor = 0

__version__ = '{major}.{minor}.{build}.{githash}'.format(major=major, minor=minor, build=build, githash=githash[:8])