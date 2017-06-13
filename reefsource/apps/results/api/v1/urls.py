from django.conf.urls import url

from .views import ResultListView, SubmitResultView

urlpatterns = [
    url(r'^$', ResultListView.as_view()),
    url(r'^submit/', SubmitResultView.as_view()),
]
