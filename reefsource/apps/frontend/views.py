import logging
from collections import OrderedDict

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect

logger = logging.getLogger(__name__)


def index(request):
    if not settings.DEBUG:
        return render(request, 'index.html')
    else:
        return redirect('http://localhost:4200/')


def is_http_header(wsgi_key):
    # The WSGI spec says that keys should be str objects in the environ dict,
    # but this isn't true in practice. See issues #449 and #482.
    return isinstance(wsgi_key, str) and wsgi_key.startswith('HTTP_')


def unmangle(wsgi_key):
    return wsgi_key[5:].replace('_', '-').title()


@user_passes_test(lambda u: u.is_superuser)
def debug(request):
    from django.views.debug import get_safe_settings

    wsgi_env = list(sorted(request.META.items()))

    request_headers = OrderedDict(
        (unmangle(k), v) for (k, v) in wsgi_env if is_http_header(k))

    return render(request, 'debug.html', context={
        'request_headers': request_headers,
        # 'response_headers': OrderedDict(sorted(response.items())),
        'settings': OrderedDict(sorted(get_safe_settings().items(), key=lambda s: s[0])),
    })
