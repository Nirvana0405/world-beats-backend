from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class UserLike(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_given_matches')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_received_matches')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} likes {self.to_user}"


class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    matched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')




# matches/models.py

class Match(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='matches_as_user2')
    matched_at = models.DateTimeField(auto_now_add=True)
