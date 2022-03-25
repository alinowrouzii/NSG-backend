from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import mixins
from knox.auth import TokenAuthentication
from product.api.serializers import (
    ColorSerializer,
    MapDesignSerializer,
    DesignSerializer,
    FontSerializer,
    ProductModelSerializer,
)
from product.models import Color, MapDesign, Design, Font, ProductModel
from rest_framework.pagination import LimitOffsetPagination


class ColorAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = ColorSerializer
    queryset = Color.objects.all()
    pagination_class = LimitOffsetPagination


class FontAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = FontSerializer
    queryset = Font.objects.all()
    pagination_class = LimitOffsetPagination


class MapDesignAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = MapDesignSerializer
    queryset = MapDesign.objects.all()
    pagination_class = LimitOffsetPagination


class DesignAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = DesignSerializer
    queryset = Design.objects.all()
    pagination_class = LimitOffsetPagination


class ProductModelAPIView(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    authentication_classes = [TokenAuthentication]
    permission_classes = (AllowAny,)
    serializer_class = ProductModelSerializer
    queryset = ProductModel.objects.all()
    pagination_class = LimitOffsetPagination