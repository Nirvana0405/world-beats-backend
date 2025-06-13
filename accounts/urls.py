# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    ActivateAPIView,  # ✅ クラスビューに統一
    LoginView,
    ProfileView,
    ProfileDetailView,
    DeactivateAccountView,
    PublicProfileView,
)

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>/", ActivateAPIView.as_view(), name="activate-user"),  # ✅ クラスビューに統一

    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-detail/", ProfileDetailView.as_view(), name="profile-detail"),
    path("deactivate/", DeactivateAccountView.as_view(), name="deactivate-account"),
    path("profiles/<int:user_id>/", PublicProfileView.as_view(), name="public-profile"),
]
