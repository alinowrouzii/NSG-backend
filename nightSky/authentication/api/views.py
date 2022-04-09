from django.contrib.auth import login

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import ValidationError
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from authentication.api.serializers import UserSerializer, ForgetPasswordVerifySerializer
from authentication.models import ForgetRecord


class LoginAPIView(KnoxLoginView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if not user.is_verified:
            raise ValidationError({"user": "user is not verified"})

        login(request, user)
        return super(LoginAPIView, self).post(request, format=None)


class RegisterAPIView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        # TODO: maybe captcha should be added to this section
        return super().create(request, *args, **kwargs)


class UserAPIView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    # queryset = User.objects

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)



class ForgetPasswordVerifyAPIView(
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordVerifySerializer
    
    def get_object(self):
        username = self.request.data.get('username', None)
        code = self.request.data.get('code', None)
        try:
            return ForgetRecord.objects.get(user__username=username, code=code, expired=False, is_used=False)
        except ForgetRecord.DoesNotExist:
            raise ValidationError({'detail': 'data is not valid'})

    
    def patch(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
