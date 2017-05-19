from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import FileUpload, AlbumList, AlbumDetail

urlpatterns = [
    url(r'^$', AlbumList.as_view()),
    url(r'^(?P<pk>\d+)/$', AlbumDetail.as_view()),
    url(r'^(?P<pk>\d+)/upload/$', FileUpload.as_view()),
]
