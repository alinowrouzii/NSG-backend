"""nightSky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from nightSky import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.api.urls')),
    path('api/v1/blog/', include('blog.api.urls')),
    path('api/v1/product/', include('product.api.urls')),
    path('api/v1/shop/', include('shop.api.urls')),
    path('api/v1/chatroom/', include('chatroom.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
