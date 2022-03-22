from django.contrib.auth import login

from rest_framework import permissions, viewsets
from rest_framework.viewsets import mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from authentication.api.serializers import UserSerializer


class LoginAPIView(
        KnoxLoginView,
        viewsets.GenericViewSet,
):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)


class RegisterAPIView(
        mixins.CreateModelMixin,
        viewsets.GenericViewSet,
):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
