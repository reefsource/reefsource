import json


from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reefsource.apps.results.models import Result
from .serializers import ResultSerializer, ResultSerializerForMap, Stage2ResultSerializer


class ResultListViewPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 1000
    max_page_size = 1000


class ResultListView(generics.ListAPIView):
    pagination_class = ResultListViewPagination
    permission_classes = (AllowAny,)
    queryset = Result.objects.filter(stage=Result.Stage.STAGE_2, success=True)
    serializer_class = ResultSerializerForMap
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('-modified',)
    ordering = ('-modified',)


class SubmitResultView(generics.CreateAPIView):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def perform_create(self, serializer):

        uploaded_file = serializer.validated_data['uploaded_file']
        stage = serializer.validated_data['stage']
        result_json = serializer.validated_data['json']

        is_valid = Result.process(uploaded_file, stage, result_json)

        getattr(uploaded_file, "{stage}_{action}".format(stage=stage, action='completed' if is_valid else 'failed'))()


