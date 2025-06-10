from rest_framework import generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import DirectMessage
from .serializers import DirectMessageSerializer, ThreadPreviewSerializer
from notifications.models import Notification

User = get_user_model()


# 🔹 1. スレッド一覧：やり取りしたユーザーごとに最新DM＋未読数
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dm_thread_list(request):
    user = request.user

    # 自分が関係しているDMの sender / receiver ID を抽出
    participants = DirectMessage.objects.filter(
        Q(sender=user) | Q(receiver=user)
    ).values_list('sender', 'receiver')

    user_ids = set()
    for sender_id, receiver_id in participants:
        if sender_id != user.id:
            user_ids.add(sender_id)
        if receiver_id != user.id:
            user_ids.add(receiver_id)

    # 相手ごとのスレッド情報を作成
    threads = []
    for uid in user_ids:
        latest_msg = DirectMessage.objects.filter(
            Q(sender=user, receiver_id=uid) | Q(sender_id=uid, receiver=user)
        ).order_by('-timestamp').first()

        unread_count = DirectMessage.objects.filter(
            sender_id=uid, receiver=user, is_read=False
        ).count()

        partner = User.objects.get(id=uid)
        threads.append({
            "user_id": uid,
            "username": partner.username,
            "last_message": latest_msg.message if latest_msg else "",
            "timestamp": latest_msg.timestamp if latest_msg else None,
            "unread_count": unread_count,
        })

    serializer = ThreadPreviewSerializer(threads, many=True)
    return Response(serializer.data)


# 🔹 2. 特定のユーザーとのDMスレッド詳細（メッセージ一覧＋未読→既読）
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dm_thread_detail(request, user_id):
    user = request.user

    # 該当ユーザーとのメッセージ一覧を取得
    messages = DirectMessage.objects.filter(
        Q(sender=user, receiver_id=user_id) | Q(sender_id=user_id, receiver=user)
    ).order_by('timestamp')

    # 相手 → 自分 の未読メッセージを既読に更新
    DirectMessage.objects.filter(
        sender_id=user_id, receiver=user, is_read=False
    ).update(is_read=True)

    serializer = DirectMessageSerializer(messages, many=True)
    return Response(serializer.data)


# 🔹 3. 新規DM作成＋一覧（ログインユーザーが関係するDMのみ）
class DirectMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = DirectMessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return DirectMessage.objects.filter(
            Q(sender=user) | Q(receiver=user)
        ).order_by('timestamp')

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)

        # 通知機能を使って受信者にDM通知を送信
        Notification.objects.create(
            to_user=message.receiver,
            message=f"{self.request.user.username} さんからDMが届きました"
        )
