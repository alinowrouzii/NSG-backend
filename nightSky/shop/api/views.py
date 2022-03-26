from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import mixins
from knox.auth import TokenAuthentication
from shop.api.serializers import OrderSerializer
from shop.models import Order


class OrderAPIView(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
        # return Order.objects.all()


class RequestPaymentAPIView():
    pass

class VerifyPaymentAPIView():
    pass