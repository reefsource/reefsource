import logging
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import logout
from django.utils import timezone

logger = logging.getLogger(__name__)


class ActiveUserMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        """
        Ensure a user not able to get in when they are not active.  If they're active logout
        """
        if request.user.is_authenticated() and not request.user.is_active:
            logout(request)

        response = self.get_response(request)

        return response

