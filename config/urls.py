# config/urls.py または project_root/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 任意：トップページ（デバッグ用）
from tracks.views import top_view

# JWT 認証ビュー
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # トップページ（開発確認用）
    path('', top_view, name='top'),

    # 管理画面
    path('admin/', admin.site.urls),

    # JWT 認証エンドポイント
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # アプリケーションAPI
    path('api/accounts/', include('accounts.urls')),         # 認証・プロフィール
    path('api/tracks/', include('tracks.urls')),             # 音楽投稿・再生
    path('api/profiles/', include('profiles.urls')),         # 他人のプロフィール閲覧
    path('api/matches/', include('matches.urls')),           # マッチング機能
    path('api/dms/', include('dms.urls')),                   # ダイレクトメッセージ機能
    path('api/notifications/', include('notifications.urls'))# 通知機能
]

# メディアファイル配信（開発時のみ）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)





# config/urls.py

urlpatterns = [
    # ...
    path('api/notifications/', include('notifications.urls')),
]




# config/urls.py

from django.contrib import admin
from django.urls import path, include
from tracks.views import top_view  # ← 追加

urlpatterns = [
    path('', top_view),  # ✅ トップページ
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/tracks/', include('tracks.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/matches/', include('matches.urls')),
    path('api/dms/', include('dms.urls')),
    path('api/notifications/', include('notifications.urls')),
]
