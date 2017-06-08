from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reefsource.apps.results.models import Result
from reefsource.core.rest_framework.permissions import CustomPermission
from .serializers import ResultSerializer, SimpleResultSerializer


class ResultListViewPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 1000
    max_page_size = 1000


class ResultListView(generics.ListAPIView):
    pagination_class = ResultListViewPagination
    permission_classes = (AllowAny,)
    queryset = Result.objects.all()
    serializer_class = SimpleResultSerializer
    filter_backends = (filters.OrderingFilter, DjangoFilterBackend)
    filter_fields = ('stage',)
    ordering_fields = ('-created',)
    ordering = ('-created',)


class Stage1ResultPermission(CustomPermission):
    required_perms = ('results.add_stage1_result',)


class Stage2ResultPermission(CustomPermission):
    required_perms = ('results.add_stage2_result',)


class AcceptStageResultsMixin():
    queryset = Result.objects.all()
    serializer_class = ResultSerializer

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AcceptStageResultsMixin, self).dispatch(request, *args, **kwargs)


class AcceptStage1ResultView(AcceptStageResultsMixin, generics.CreateAPIView):
    permission_classes = (Stage1ResultPermission,)

    @transaction.atomic
    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data['uploaded_file']
        results = uploaded_file.stage1_completed()

        serializer.save(json=results, stage=Result.Stage.STAGE_1)


class AcceptStage2ResultView(AcceptStageResultsMixin, generics.CreateAPIView):
    permission_classes = (Stage2ResultPermission,)

    @transaction.atomic
    def perform_create(self, serializer):
        uploaded_file = serializer.validated_data['uploaded_file']
        results = uploaded_file.stage2_completed()

        lat = results.get('GPSLatitude', 0)
        lng = results.get('GPSLongitude', 0)
        score = results.get('score', -1)

        serializer.save(json=results, lat=lat, lng=lng, score=score, stage=Result.Stage.STAGE_2)
