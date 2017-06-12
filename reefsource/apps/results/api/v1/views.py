import json

from django.contrib.gis.geos import Point
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reefsource.apps.results.models import Result
from .serializers import ResultSerializer, ResultSerializerForMap


class ResultListViewPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 1000
    max_page_size = 1000


class ResultListView(generics.ListAPIView):
    pagination_class = ResultListViewPagination
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = ResultSerializerForMap
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('stage',)
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
        stage = serializer.validated_data['stage']
        uploaded_file = serializer.validated_data['uploaded_file']
        contents = json.loads(serializer.validated_data['json'])

        getattr(uploaded_file, "{stage}_{action}".format(stage=stage, action='completed' if 'error' not in contents else 'failed'))()

        Result.objects.update_or_create(uploaded_file=uploaded_file, defaults={
            'stage': stage,
            'json': contents,
            'location': Point(x=contents.get('GPSLatitude', None), y=contents.get('GPSLongitude', None), srid=4326),
            'score': contents.get('score', None)
        })
