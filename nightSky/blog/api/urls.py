from django.urls import include, path
from blog.api.views import index

urlpatterns = [
    path("", index)
]
