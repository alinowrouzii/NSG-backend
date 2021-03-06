from django.urls import path
from shop.api.views import OrderAPIView, RequestPaymentAPIView, VerifyPaymentAPIView

urlpatterns = [
    path("order/", OrderAPIView.as_view({"get": "list", "post": "create"})),
    path("order/<pk>/", OrderAPIView.as_view({"get": "retrieve"})),
    path("payment/request/<pk>", RequestPaymentAPIView.as_view()),
    path("payment/verify/", VerifyPaymentAPIView.as_view()),
]
