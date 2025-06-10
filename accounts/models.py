from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from tracks.models import Track
from django.db.models import JSONField  # SQLite対応のJSONField

# ✅ カスタムユーザーモデル
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)  # デフォルトで有効に
    USERNAME_FIELD = 'username'  # 明示的に指定（デフォルトと同じでもOK）

# ✅ プロフィールモデル
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # ← ここでカスタムユーザーを参照
        on_delete=models.CASCADE,
        related_name='account_profile'
    )
    display_name = models.CharField(max_length=50)
    bio = models.TextField(blank=True)
    icon = models.ImageField(upload_to='profile_icons/', blank=True, null=True)

    favorite_genres = JSONField(default=list, blank=True)  # SQLiteでも対応可能
    favorite_artists = models.CharField(max_length=255, blank=True)

    best_track = models.ForeignKey(
        Track,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.display_name or self.user.username
