from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, generics
from rest_framework.viewsets import mixins
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from knox.auth import TokenAuthentication
from blog.models import Post, Comment
from blog.api.serializers import CommentSerializer, PostSerializer, PostSerializerMinimal
from rest_framework.pagination import LimitOffsetPagination

# Create your views here.


class PostAPIView(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PostListAPIView(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = PostSerializerMinimal
    queryset = Post.objects.all().order_by('-timestamp')
    pagination_class = LimitOffsetPagination
    
    


class CommentAPIView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer
    queryset = Comment.objects.all().order_by('-timestamp')
    