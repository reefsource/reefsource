from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import FileUpload, AlbumListView, AlbumDetailView, FileUploadView

urlpatterns = [
    url(r'^$', AlbumListView.as_view()),
    url(r'^(?P<pk>\d+)/$', AlbumDetailView.as_view()),
    url(r'^(?P<albumId>\d+)/upload/$', FileUpload.as_view()),

    url(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view())
]
