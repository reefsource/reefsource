from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import AlbumListView, AlbumDetailView, FileUploadView, FileUploadViewDetailView, FileUploadReanalyzeView

urlpatterns = [
    url(r'^$', AlbumListView.as_view()),
    url(r'^(?P<pk>\d+)/$', AlbumDetailView.as_view()),
    url(r'^(?P<albumId>\d+)/upload/$', FileUploadView.as_view()),
    url(r'^(?P<albumId>\d+)/upload/(?P<pk>\d+)/$', FileUploadViewDetailView.as_view()),
    url(r'^(?P<albumId>\d+)/upload/(?P<pk>\d+)/reanalyze/$', FileUploadReanalyzeView.as_view()),
]
