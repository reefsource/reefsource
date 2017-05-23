from django.conf.urls import url

from .views import ResultListView, AcceptStage1ResultView, AcceptStage2ResultView

urlpatterns = [
    url(r'^$', ResultListView.as_view()),
    url(r'^stage1complete/$', AcceptStage1ResultView.as_view()),
    url(r'^stage2complete/$', AcceptStage2ResultView.as_view()),
]
