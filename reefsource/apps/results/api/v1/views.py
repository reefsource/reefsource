from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.permissions import AllowAny

from reefsource.apps.results.models import Result
from .serializers import ResultSerializer


class ResultListView(generics.ListAPIView):
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer


class AcceptStageResultsMixin():
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AcceptStageResultsMixin, self).dispatch(request, *args, **kwargs)


class AcceptStage1ResultView(AcceptStageResultsMixin, generics.CreateAPIView):
    @transaction.atomic
    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data['uploaded_file']
        results = uploaded_file.stage1_completed()

        serializer.save(json=results)


class AcceptStage2ResultView(AcceptStageResultsMixin, generics.CreateAPIView):
    @transaction.atomic
    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data['uploaded_file']
        results = uploaded_file.stage2_completed()

        serializer.save(json=results)
