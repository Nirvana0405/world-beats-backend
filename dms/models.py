from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL  # カスタムユーザーモデルを参照

class DirectMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # 既読フラグ

    def __str__(self):
        return f"From {self.sender} to {self.receiver}: {self.message[:30]}"
