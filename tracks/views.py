from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import get_user_model

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import Track, TrackLike, PlayHistory, Comment, UserLike
from .serializers import (
    TrackSerializer,
    PlayHistorySerializer,
    CommentSerializer,
    MatchUserSerializer,  # ← ✅ 追加
)

User = get_user_model()

# ============================
# 📄 トップページ
# ============================
def top_view(request):
    return HttpResponse("🎷 WORLD_BEATS API トップページへようこそ！")


# ============================
# 🎵 Track 関連
# ============================
class TrackListCreateView(generics.ListCreateAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.AllowAny]

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class TrackDetailView(RetrieveAPIView):
    queryset = Track.objects.all()
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserTrackListView(generics.ListAPIView):
    serializer_class = TrackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Track.objects.filter(uploaded_by=self.request.user)


@api_view(['GET'])
@permission_classes([AllowAny])
def top_liked_tracks(request):
    tracks = Track.objects.annotate(num_likes=Count("track_likes")).order_by("-num_likes")[:10]
    serializer = TrackSerializer(tracks, many=True, context={"request": request})
    return Response(serializer.data)


# ============================
# ❤️ Like 関連
# ============================
class LikeTrackView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        track = get_object_or_404(Track, pk=pk)
        user = request.user
        like, created = TrackLike.objects.get_or_create(user=user, track=track)

        if not created:
            like.delete()
            return Response({'message': 'Like removed'}, status=200)

        return Response({'message': 'Like added'}, status=201)


# ============================
# ▶️ 再生履歴 関連
# ============================
class PlayHistoryListView(generics.ListAPIView):
    serializer_class = PlayHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PlayHistory.objects.filter(user=self.request.user)


class PlayHistoryCreateView(generics.CreateAPIView):
    serializer_class = PlayHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================
# 💬 コメント 関連
# ============================
class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        track_id = self.request.query_params.get('track_id')
        if track_id:
            return Comment.objects.filter(track_id=track_id)
        return Comment.objects.all()


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


# ============================
# 💘 マッチング 関連
# ============================
class MatchListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_users = UserLike.objects.filter(from_user=user).values_list('to_user', flat=True)
        liked_by_users = UserLike.objects.filter(to_user=user).values_list('from_user', flat=True)
        matched_user_ids = set(liked_users).intersection(set(liked_by_users))
        matched_users = User.objects.filter(id__in=matched_user_ids)

        serializer = MatchUserSerializer(matched_users, many=True)
        return Response(serializer.data)




# tracks/views.py
from rest_framework import generics, permissions
from .models import Like
from .serializers import LikeSerializer

class LikeTrackView(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)
