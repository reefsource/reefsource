from django.conf.urls import url

from .views import ResultListView, AcceptResultView

urlpatterns = [
    url(r'^', ResultListView.as_view()),
    url(r'^stage1complete', AcceptResultView.as_view()),
    url(r'^stage2complete', AcceptResultView.as_view()),
]
