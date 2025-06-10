from rest_framework import serializers
from .models import DirectMessage
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ユーザー情報をネストで返すための簡易Serializer（必要に応じて拡張可）"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class DirectMessageSerializer(serializers.ModelSerializer):
    """DMの送受信データ用シリアライザ"""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)

    class Meta:
        model = DirectMessage
        fields = ['id', 'sender', 'receiver', 'message', 'timestamp', 'is_read']
        read_only_fields = ['id', 'sender', 'timestamp', 'is_read']


class ThreadPreviewSerializer(serializers.Serializer):
    """スレッド一覧表示用（未読数・最新メッセージ付き）"""
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    last_message = serializers.CharField()
    timestamp = serializers.DateTimeField()
    unread_count = serializers.IntegerField()
