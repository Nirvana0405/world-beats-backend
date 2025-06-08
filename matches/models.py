from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserLike(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given_matches')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received_matches')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} likes {self.to_user}"
