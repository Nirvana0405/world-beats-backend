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
    MatchUserSerializer,
)

User = get_user_model()

# ----------------------------
# トップページ（テスト用）
# ----------------------------
def top_view(request):
    return HttpResponse("🎷 WORLD_BEATS API トップページへようこそ！")


# ----------------------------
# 🎵 トラック関連
# ----------------------------
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
    try:
        tracks = Track.objects.annotate(
            num_likes=Count('track_likes')  # ← related_name='track_likes' が TrackLike に必要
        ).order_by('-num_likes')[:10]

        serializer = TrackSerializer(tracks, many=True, context={"request": request})
        return Response(serializer.data)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


# ----------------------------
# ❤️ Like 機能
# ----------------------------
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


# ----------------------------
# ▶️ 再生履歴
# ----------------------------
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


# ----------------------------
# 💬 コメント機能
# ----------------------------
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


# ----------------------------
# 💘 マッチング機能
# ----------------------------
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



# tracks/views.py などの Like API の中で使用

from matches.utils import create_match_if_mutual

class LikeTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, track_id):
        track = get_object_or_404(Track, id=track_id)
        to_user = track.uploaded_by
        from_user = request.user

        # すでにLikeしていたら削除（トグル式にする場合）
        existing = Like.objects.filter(from_user=from_user, to_user=to_user, track=track)
        if existing.exists():
            existing.delete()
            return Response({"message": "💔 Likeを取り消しました"}, status=200)

        # Likeを新規作成
        Like.objects.create(from_user=from_user, to_user=to_user, track=track)

        # 💡 マッチング成立していれば Match を作成
        create_match_if_mutual(from_user, to_user)

        return Response({"message": "❤️ Likeしました"}, status=201)



from matches.utils import create_match_if_mutual




# tracks/views.py

from django.http import HttpResponse

def top_view(request):
    return HttpResponse("🎵 World Beats API サーバーは動作中です")
