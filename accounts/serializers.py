from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile  # ← ✅ 正しいモデルに修正
from tracks.models import Track

User = get_user_model()

# ✅ ユーザー登録用シリアライザ
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

# ✅ ユーザー情報表示用（プロフィール画面などで使用）
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

# ✅ プロフィール表示・編集用
class ProfileSerializer(serializers.ModelSerializer):
    icon = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'display_name',
            'bio',
            'icon',
            'favorite_genres',
            'favorite_artists',
            'best_track'
        ]

# ✅ トラック用シリアライザ
class TrackSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'like_count', 'is_liked', 'audio_file', 'created_at']

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False
