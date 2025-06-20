from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracks.views import top_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 📄 トップページ (APIやデバッグ用)
    path('', top_view, name='top'),

    # 📖 管理画面
    path('admin/', admin.site.urls),

    # 🔐 JWT 認証API
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 📁 各機能アプリのAPI
    path('api/accounts/', include('accounts.urls')),
    path('api/tracks/', include('tracks.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/matches/', include('matches.urls')),
    path('api/dms/', include('dms.urls')),
    path('api/notifications/', include('notifications.urls')),
]

# 🚧 開発時のメディアファイル配信
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
