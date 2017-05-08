"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken import views

# todo make login and logout go directly to root directly
admin.site.login = login_required(admin.site.login)
# admin.site.logout = remove

import reefsource.apps.frontend.views

from rest_framework_swagger.views import get_swagger_view

urlpatterns = [
    url(r'^api/v1/docs/$', get_swagger_view(title='reefsource API')),

    url(r'^api/v1/users/', include('reefsource.apps.users.api.v1.urls')),

    url(r'^ht/', include('health_check.urls')),

    url(r'^oauth2/', include('social_django.urls', namespace='social')),
    url(r'^token-auth/$', views.obtain_auth_token),

    url(r'^admin/', admin.site.urls),
    url(r'debug', reefsource.apps.frontend.views.debug),

    url(r'^.*$', reefsource.apps.frontend.views.index, name='home'),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [url(r'^__debug__/', include(debug_toolbar.urls))] + urlpatterns

    from django.conf.urls.static import static

    urlpatterns = static('/media/', document_root=settings.MEDIA_ROOT) + urlpatterns

    urlpatterns = static('/reefsource/apps/frontend/angular/', document_root='./reefsource/apps/frontend/angular') + urlpatterns
    urlpatterns = static('/node_modules/', document_root='./node_modules') + urlpatterns
