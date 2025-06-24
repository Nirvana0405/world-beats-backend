# accounts/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    ActivateAPIView,
    LoginView,
    ProfileView,
    ProfileDetailView,
    DeactivateAccountView,
    PublicProfileView,
    ProfileRetrieveUpdateView,  # ← 忘れずに追加
)

urlpatterns = [
    # 🔐 JWTトークン
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 👤 アカウント管理
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>/", ActivateAPIView.as_view(), name="activate-user"),
    path("login/", LoginView.as_view(), name="login"),
    path("deactivate/", DeactivateAccountView.as_view(), name="deactivate-account"),

    # 🙍‍♀️ プロフィール関連
    path("profile/", ProfileView.as_view(), name="profile"),  # 自分のプロフィール取得用（GET）
    path("profile-detail/", ProfileDetailView.as_view(), name="profile-detail"),  # 画像アップロードなど
    path("profiles/<int:user_id>/", PublicProfileView.as_view(), name="public-profile"),  # 他人のプロフィール
    path("profile-edit/", ProfileRetrieveUpdateView.as_view(), name="profile-edit"),  # PATCH など編集用
]
