from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tracks.models import Track
from django.db.models import JSONField  # ← SQLite対応のJSONFieldを使用

# ✅ カスタムユーザーモデル
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  # ← デフォルトでログイン可能に
    USERNAME_FIELD = 'username'  # 明示しておくと安心

# ✅ プロフィールモデル
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='account_profile'
    )
    display_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    icon = models.ImageField(upload_to='profile_icons/', blank=True, null=True)

    # ✅ JSONField に変更（SQLiteでも動作可能）
    favorite_genres = JSONField(default=list, blank=True)

    favorite_artists = models.CharField(max_length=255, blank=True)

    # ✅ ベストトラック（任意）
    best_track = models.ForeignKey(
        Track,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.display_name or self.user.username
