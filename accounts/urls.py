from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView,
    activate_user,
    LoginView,
    ProfileView,         # ✅ PATCH対応（表示名、ジャンル、アーティストなど）
    ProfileDetailView,   # ✅ PUT対応（画像アップロードなど）
)

urlpatterns = [
    # 🔐 JWT 認証エンドポイント
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 📝 ユーザー登録 + アクティベーション（メール）
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:token>/', activate_user, name='activate-user'),

    # 🧪 簡易ログイン（開発・テスト用）
    path('login/', LoginView.as_view(), name='login'),

    # 👤 プロフィール取得・更新（JSON形式：PATCH）
    path('profile/', ProfileView.as_view(), name='profile'),

    # 🖼️ プロフィール画像やMultipart用（Form形式：PUT）
    path('profile-detail/', ProfileDetailView.as_view(), name='profile-detail'),
]
