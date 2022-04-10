from django.urls import include, path
from authentication.api.views import (
    LoginAPIView,
    RegisterAPIView,
    UserAPIView,
    ForgetPasswordVerifyAPIView,
    ForgetPasswordRequestAPIView,
)

# router = routers.SimpleRouter()
# router.register('register/', RegisterAPIView, basename="register")
# router.register('login/', LoginAPIView, basename="login")
# urlpatterns = router.urls


urlpatterns = [
    path("", UserAPIView.as_view({"get": "get", "patch": "patch"})),
    path("login/", LoginAPIView.as_view()),
    path("register/", RegisterAPIView.as_view({"post": "create"})),
    path("forget/request/", ForgetPasswordRequestAPIView.as_view({"post": "post"})),
    path("forget/verify/", ForgetPasswordVerifyAPIView.as_view({"patch": "patch"})),
]
