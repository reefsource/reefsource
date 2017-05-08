import os

os.environ.setdefault('POSTGRES_HOST', 'postgres')
os.environ.setdefault('REDIS_HOST', 'redis')
os.environ.setdefault('RABBIT_HOST', 'rabbitmq')

from reefsource.settings.base import *