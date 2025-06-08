from django.urls import path
from .views import (
    TrackListCreateView,
    TrackDetailView,
    UserTrackListView,
    LikeTrackView,
    PlayHistoryListView,
    PlayHistoryCreateView,
    CommentCreateView,
    CommentListView,
    CommentDeleteView,
    top_liked_tracks,     # 🔥 人気トラック表示
    top_view,             # 🔧 テスト用トップページ
)

urlpatterns = [
    # テストトップページ
    path('top/', top_view, name='top-view'),

    # トラック機能
    path('', TrackListCreateView.as_view(), name='track-list-create'),
    path('<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('my/', UserTrackListView.as_view(), name='my-tracks'),
    path('top-liked/', top_liked_tracks, name='top-liked'),

    # Like機能
    path('<int:pk>/like/', LikeTrackView.as_view(), name='track-like'),

    # 再生履歴
    path('history/', PlayHistoryListView.as_view(), name='play-history'),
    path('history/add/', PlayHistoryCreateView.as_view(), name='add-history'),

    # コメント機能
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/add/', CommentCreateView.as_view(), name='comment-add'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]






from .views import MatchListView

urlpatterns += [
    path('matches/', MatchListView.as_view(), name='match-list'),
]




from django.urls import path
from .views import (
    top_view,
    TrackListCreateView, TrackDetailView, UserTrackListView,
    top_liked_tracks,
    LikeTrackView,
    PlayHistoryListView, PlayHistoryCreateView,
    CommentCreateView, CommentListView, CommentDeleteView,
    MatchListView,  # ← 追加
)

urlpatterns = [
    path('top/', top_view, name='top'),
    path('tracks/', TrackListCreateView.as_view(), name='track-list-create'),
    path('tracks/<int:pk>/', TrackDetailView.as_view(), name='track-detail'),
    path('tracks/my/', UserTrackListView.as_view(), name='my-tracks'),
    path('tracks/top-liked/', top_liked_tracks, name='top-liked'),
    path('tracks/<int:pk>/like/', LikeTrackView.as_view(), name='like-track'),
    path('play-history/', PlayHistoryListView.as_view(), name='play-history-list'),
    path('play-history/create/', PlayHistoryCreateView.as_view(), name='play-history-create'),
    path('comments/', CommentListView.as_view(), name='comment-list'),
    path('comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('matches/', MatchListView.as_view(), name='match-list'),  # ✅ ここ
]






# tracks/urls.py
from .views import LikeTrackView

urlpatterns = [
    # ...他のURL
    path('like/', LikeTrackView.as_view(), name='like-user'),
]
