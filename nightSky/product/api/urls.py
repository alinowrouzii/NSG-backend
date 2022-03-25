from django.urls import path
from product.api.views import *

urlpatterns = [
   path('color/', ColorAPIView.as_view({"get":"list"})),
   path('color/<pk>/', ColorAPIView.as_view({"get":"retrieve"})),
   path('font/', FontAPIView.as_view({"get":"list"})),
   path('font/<pk>/', FontAPIView.as_view({"get":"retrieve"})),
   path('design/', DesignAPIView.as_view({"get":"list"})),
   path('design/<pk>/', DesignAPIView.as_view({"get":"retrieve"})),
   path('map_design/', MapDesignAPIView.as_view({"get":"list"})),
   path('map_design/<pk>/', MapDesignAPIView.as_view({"get":"retrieve"})),
   path('product_model/', ProductModelAPIView.as_view({"get":"list"})),
   path('product_model/<pk>/', ProductModelAPIView.as_view({"get":"retrieve"})),
]
