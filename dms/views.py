from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from .models import DirectMessage
from .serializers import DirectMessageSerializer
from notifications.models import Notification

class DirectMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # 自分が送信者または受信者のDMを取得
        return DirectMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('timestamp')

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)

        # ✅ 受信者に通知を送信
        Notification.objects.create(
            to_user=message.receiver,
            message=f"{self.request.user.username} さんからDMが届きました"
        )
