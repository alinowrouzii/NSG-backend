from django.urls import path
from shop.api.views import OrderAPIView

urlpatterns = [
    path("", OrderAPIView.as_view({"get": "list", "post": "create"})),
    path("<pk>/", OrderAPIView.as_view({"get": "retrieve"})),
]
