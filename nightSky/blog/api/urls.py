from django.urls import include, path
from blog.api.views import PostAPIView, PostListAPIView, CommentAPIView

urlpatterns = [
    path("post/", PostListAPIView.as_view({'get': 'list'})),
    path("post/<pk>/", PostAPIView.as_view({'get': 'get'})),
    path("comment/", CommentAPIView.as_view({'post': 'create'}))
]
