from django.urls import path
from .views import (
    top_view,
    TrackListCreateView,
    TrackDetailView,
    UserTrackListView,
    LikeTrackView,
    PlayHistoryListView,
    PlayHistoryCreateView,
    CommentCreateView,
    CommentListView,
    CommentDeleteView,
    top_liked_tracks,
    MatchListView,
)

urlpatterns = [
    # 🎧 トップページ（開発用）
    path('top/', top_view, name='top'),

    # 🎵 トラック関連
    path('', TrackListCreateView.as_view(), name='track-list-create'),
    path('<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('my/', UserTrackListView.as_view(), name='my-tracks'),
    path('top-liked/', top_liked_tracks, name='top-liked'),
    path('<int:pk>/like/', LikeTrackView.as_view(), name='track-like'),

    # ▶️ 再生履歴
    path('history/', PlayHistoryListView.as_view(), name='play-history'),
    path('history/add/', PlayHistoryCreateView.as_view(), name='add-history'),

    # 💬 コメント関連
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/add/', CommentCreateView.as_view(), name='comment-add'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),

    # 💘 マッチング機能
    path('matches/', MatchListView.as_view(), name='match-list'),
]
