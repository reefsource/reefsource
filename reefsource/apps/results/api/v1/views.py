from rest_framework import generics
from rest_framework.permissions import AllowAny

from reefsource.apps.results.models import Result
from .serializers import ResultSerializer


class ResultListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class AcceptResultView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    def create(self, request, *args, **kwargs):
        super()