from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    activate_user,
    LoginView,
    ProfileView,
    ProfileDetailView,
    DeactivateAccountView,
)

urlpatterns = [
    # 🔐 JWT 認証エンドポイント
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # 📝 ユーザー登録 ＋ アクティベーション（メール）
    path("register/", RegisterView.as_view(), name="register"),
    path("activate/<str:token>/", activate_user, name="activate-user"),

    # 🧪 ログイン（開発・テスト用 or 拡張版）
    path("login/", LoginView.as_view(), name="login"),

    # 👤 プロフィール（JSON：PATCH対応）
    path("profile/", ProfileView.as_view(), name="profile"),

    # 🖼️ プロフィール詳細（画像付きPUT用）
    path("profile-detail/", ProfileDetailView.as_view(), name="profile-detail"),

    # ❌ アカウント退会（DELETEで is_active=False）
    path("deactivate/", DeactivateAccountView.as_view(), name="deactivate-account"),
]




# accounts/urls.py
from .views import PublicProfileView

urlpatterns += [
    path("public-profile/<int:user_id>/", PublicProfileView.as_view(), name="public-profile"),
]
