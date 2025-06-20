from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class MatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # 必要に応じて拡張




# matches/serializers.py

from rest_framework import serializers
from accounts.serializers import PublicProfileSerializer
from .models import Match

class MatchSerializer(serializers.ModelSerializer):
    matched_user = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = ['id', 'matched_user', 'matched_at']

    def get_matched_user(self, obj):
        request_user = self.context['request'].user
        other_user = obj.user2 if obj.user1 == request_user else obj.user1
        from accounts.models import Profile
        profile = Profile.objects.get(user=other_user)
        return PublicProfileSerializer(profile).data

