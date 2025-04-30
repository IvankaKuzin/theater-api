from django.urls import path
from user.views import CreateUserView, CreateTokenView, ManageUserView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

app_name = "user"

urlpatterns = [
    path("registers/", CreateUserView.as_view(), name="create"),
    path("tokens/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("tokens/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("tokens/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("me/", ManageUserView.as_view(), name="manage"),
]
