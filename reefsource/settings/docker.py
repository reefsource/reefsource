import os

os.environ.setdefault('POSTGRES_HOST', 'postgres')
os.environ.setdefault('REDIS_HOST', 'redis')
os.environ.setdefault('RABBIT_HOST', 'rabbitmq')

from reefsource.settings.base import *

#proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

#https

SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_BROWSER_XSS_FILTER = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

NEW_RELIC_CONFIG_FILE='newrelic.ini'

# https://dryan.com/articles/elb-django-allowed-hosts/
import requests
EC2_PRIVATE_IP  =   None
try:
    EC2_PRIVATE_IP  =   requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout = 0.01).text
except requests.exceptions.RequestException:
    pass

if EC2_PRIVATE_IP:
    ALLOWED_HOSTS.append(EC2_PRIVATE_IP)
    
