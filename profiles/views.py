from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Profile
from .serializers import ProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile




from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from django.contrib.auth import get_user_model

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # ログイン中のユーザーのプロフィールを返す
        return self.request.user.profile

# profiles/views.py
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(APIView):
    permission_classes = [AllowAny]  # 本番では IsAuthenticated に変更

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)








from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class OtherUserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        profile = Profile.objects.get(user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)






# profiles/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from django.shortcuts import get_object_or_404

class OtherUserProfileView(APIView):
    permission_classes = [AllowAny]  # 必要に応じて IsAuthenticated に変更

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)




# profiles/views.py

from rest_framework.generics import RetrieveAPIView
from accounts.models import Profile
from .serializers import PublicProfileSerializer

class PublicProfileView(RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer
    lookup_field = 'user__id'  # ユーザーIDで取得







# profiles/views.py
from rest_framework import generics, permissions
from accounts.models import Profile
from accounts.serializers import ProfileSerializer

class OtherUserProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)



# profiles/views.py
from rest_framework import generics, permissions, filters
from .models import Profile
from .serializers import ProfileSerializer

class PublicProfileListView(generics.ListAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['display_name', 'favorite_genres', 'favorite_artists']




# profiles/views.py
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.select_related("user")
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]




# profiles/views.py

from rest_framework.generics import RetrieveAPIView
from accounts.models import Profile
from accounts.serializers import PublicProfileSerializer

class PublicProfileDetailView(RetrieveAPIView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = PublicProfileSerializer
    lookup_field = 'user_id'  # URLのidに対応

