from rest_framework import generics, permissions, filters, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404

from accounts.models import Profile
from accounts.serializers import ProfileSerializer, PublicProfileSerializer

# ◆ プロファイルがなければ作成

def get_or_create_profile(user):
    return Profile.objects.get_or_create(user=user)[0]

# =============================
# 🔑 自分のプロフィール取得/更新
# =============================
class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_or_create_profile(self.request.user)

# =============================
# 👤 他人プロフィール一覧
# =============================
class OtherUserProfilesView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.exclude(user=self.request.user)

# =============================
# 🔍 公開プロフィール検索
# =============================
class PublicProfileListView(generics.ListAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['display_name', 'favorite_genres', 'favorite_artists']

# =============================
# 🔍 公開プロフィール個別
# =============================
class PublicProfileDetailView(generics.RetrieveAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = PublicProfileSerializer
    permission_classes = [AllowAny]
    lookup_field = 'user_id'  # URL /profiles/<user_id>/

# =============================
# → APIのテスト用: 全プロフィール
# =============================
class AllProfilesDebugView(APIView):
    permission_classes = [AllowAny]  # 本番では禁止

    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)

# =============================
# 👁 他人プロフィール個別
# =============================
class OtherUserProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
