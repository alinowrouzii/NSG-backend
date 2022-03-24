from django.contrib.auth import login

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import mixins
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from authentication.api.serializers import UserSerializer
from authentication.models import User
from shop.api.serializers import OrderWriteSerializer, OrderReadSerializer
from shop.models import Order


class OrderAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderWriteSerializer
    
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        # return Order.objects.all()


