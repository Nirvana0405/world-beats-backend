from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    activate_user,  # ✅ ← ActivateAPIView は削除し、関数ビューを使用
    LoginView,
    ProfileView,
    ProfileDetailView,
    DeactivateAccountView,
    PublicProfileView,
)

urlpatterns = [
    # 🔐 JWT 認証エンドポイント
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📝 ユーザー登録＋アクティベーション
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>/", activate_user, name="activate-user"),

    # 🧪 ログイン（開発・テスト用）
    path("login/", LoginView.as_view(), name="login"),

    # 👤 プロフィール関連
    path("profile/", ProfileView.as_view(), name="profile"),
    path("profile-detail/", ProfileDetailView.as_view(), name="profile-detail"),

    # ❌ アカウント退会
    path("deactivate/", DeactivateAccountView.as_view(), name="deactivate-account"),

    # 🌍 他人プロフィール
    path("profiles/<int:user_id>/", PublicProfileView.as_view(), name="public-profile"),
]
