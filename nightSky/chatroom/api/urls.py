from django.urls import path
from chatroom.api.views import MessageAPIView

urlpatterns = [
    path("", MessageAPIView.as_view({"post": "post", "get": "list"})),
    path("<pk>/", MessageAPIView.as_view({"get": "retrieve"})),
]
