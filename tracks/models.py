from django.db import models
from django.conf import settings

# ユーザー
User = settings.AUTH_USER_MODEL


# 🎵 楽曲モデル
class Track(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tracks',
    )
    audio_file = models.FileField(upload_to='tracks/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

    def like_count(self):
        return self.track_likes.count()  # 関連名を合わせる


# ❤️ 楽曲へのLike（Track用）
class TrackLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='track_likes')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='track_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} liked {self.track.title}"


# ▶️ 再生履歴
class PlayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    played_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} played {self.track.title} at {self.played_at}"


# 💬 コメント
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.track.title}: {self.text[:20]}"


# 💘 ユーザー同士のLike（マッチング用）
class UserLike(models.Model):
    from_user = models.ForeignKey(User, related_name='likes_given', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='likes_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"





# tracks/models.py など

class Like(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')  # 重複Like防止




class Like(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received_from_like')
    created_at = models.DateTimeField(auto_now_add=True)


class UserLike(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userlikes_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received_from_userlike')
    created_at = models.DateTimeField(auto_now_add=True)
