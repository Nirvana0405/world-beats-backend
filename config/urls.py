from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 任意：トップページビュー（デバッグ用）
from tracks.views import top_view

# JWT 認証ビュー（必要に応じて修正）
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 🏠 トップページ（開発時のテスト表示などに使用）
    path('', top_view, name='top'),

    # 🔐 管理画面
    path('admin/', admin.site.urls),

    # 🔐 JWT 認証
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 📦 各アプリのAPIエンドポイント
    path('api/accounts/', include('accounts.urls')),        # アカウント関連（登録・ログイン・プロフィール）
    path('api/tracks/', include('tracks.urls')),            # 音楽投稿・再生
    path('api/profiles/', include('profiles.urls')),        # 他人プロフィール表示（任意）
    path('api/matches/', include('matches.urls')),          # マッチング機能
    path('api/dms/', include('dms.urls')),                  # DM機能
    path('api/notifications/', include('notifications.urls')),  # ✅ 通知機能 ← 追加済み！
]

# 📁 メディアファイル配信設定（開発環境のみ）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
