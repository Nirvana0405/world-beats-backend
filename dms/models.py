# dms/models.py
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # カスタムユーザーモデルを参照

class DirectMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_direct_messages',  # 他モデルと重複しないよう命名
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_direct_messages',  # 同上
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} → {self.receiver}: {self.message[:30]}"
