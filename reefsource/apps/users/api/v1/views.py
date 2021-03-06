import logging

from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import renderers, parsers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reefsource.apps.users.api.v1.serializers import UserProfileSerializer, LoginSerializer
from reefsource.apps.users.models import User

logger = logging.getLogger(__name__)


class LoginView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        response_data = UserProfileSerializer(user).data
        return Response(response_data)


class LogoutView(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        logout(request)
        return Response({})


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    pagination_class = (None,)
    queryset = User.objects.all()

    def get_queryset(self):
        queryset = super(UserProfileView, self).get_queryset()
        queryset = queryset.filter(pk=self.request.user.id)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        return get_object_or_404(queryset)

    def update(self, request, *args, **kwargs):
        instance = request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
