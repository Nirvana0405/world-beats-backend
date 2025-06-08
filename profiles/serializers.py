from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.models import Profile
from tracks.models import Track

User = get_user_model()

# 🔹 ユーザー情報（限定的）
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 🔹 シンプルなTrack情報（再生用）
class TrackSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'audio_file']

# 🔹 ログインユーザー自身のプロフィール表示・編集用
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'avatar', 'bio']
        read_only_fields = ['id']

# 🔹 他人のプロフィール公開用（＋投稿一覧つき）
class PublicProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    tracks = TrackSimpleSerializer(source='user.track_set', many=True)

    class Meta:
        model = Profile
        fields = [
            'user_id',
            'display_name',
            'bio',
            'icon',
            'favorite_genres',
            'favorite_artists',
            'tracks',
        ]
