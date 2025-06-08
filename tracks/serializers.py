from rest_framework import serializers
from .models import Track, TrackLike, PlayHistory, Comment, Like
from django.contrib.auth import get_user_model

User = get_user_model()


# 🎵 楽曲シリアライザ
class TrackSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    audio_file = serializers.SerializerMethodField()
    uploaded_by_username = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = [
            'id', 'title', 'artist', 'audio_file',
            'like_count', 'is_liked',
            'uploaded_by', 'uploaded_by_username',
            'created_at'
        ]
        read_only_fields = [
            'id', 'uploaded_by', 'uploaded_by_username',
            'created_at', 'like_count', 'is_liked'
        ]

    def get_like_count(self, obj):
        return obj.track_likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.track_likes.filter(user=request.user).exists()
        return False

    def get_audio_file(self, obj):
        request = self.context.get('request')
        if obj.audio_file and request:
            return request.build_absolute_uri(obj.audio_file.url)
        return None

    def get_uploaded_by_username(self, obj):
        return obj.uploaded_by.username if obj.uploaded_by else None

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['uploaded_by'] = request.user
        return super().create(validated_data)


# ▶️ 再生履歴シリアライザ
class PlayHistorySerializer(serializers.ModelSerializer):
    track_title = serializers.CharField(source='track.title', read_only=True)

    class Meta:
        model = PlayHistory
        fields = ['id', 'user', 'track', 'track_title', 'played_at']
        read_only_fields = ['id', 'played_at']


# 💬 コメントシリアライザ
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    track = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'track', 'text', 'created_at']
        read_only_fields = ['id', 'user', 'track', 'created_at']


# ❤️ Trackに対するいいね（TrackLike）シリアライザ
class TrackLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackLike
        fields = '__all__'


# 👤 ユーザーマッチング用シリアライザ
class MatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# ❤️ ユーザー間のLike（マッチング用）シリアライザ
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'from_user', 'to_user', 'created_at']
        read_only_fields = ['from_user', 'created_at']
