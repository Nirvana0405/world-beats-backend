from django.test import TestCase

# Create your tests here.
# profiles/serializers.py

from rest_framework import serializers
from accounts.models import Profile
from tracks.models import Track

class TrackSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ['id', 'title', 'artist', 'audio_file']

class PublicProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    tracks = TrackSimpleSerializer(source='user.track_set', many=True)

    class Meta:
        model = Profile
        fields = ['user_id', 'display_name', 'bio', 'icon', 'favorite_genres', 'favorite_artists', 'tracks']
