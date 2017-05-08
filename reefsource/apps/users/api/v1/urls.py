from __future__ import unicode_literals, absolute_import

from django.conf.urls import url

from .views import UserList, UserDetail, UserProfileView, LogoutView, LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', UserProfileView.as_view(), name='user_profile'),

    url(r'^$', UserList.as_view(), name='user_list'),
    url(r'^(?P<pk>\d+)/$', UserDetail.as_view(), name='user_detail'),
]
