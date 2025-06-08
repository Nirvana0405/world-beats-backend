from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class MatchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # 必要に応じて拡張





