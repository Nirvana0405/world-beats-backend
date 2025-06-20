# matches/urls.py

from django.urls import path
from .views import MatchListView

urlpatterns = [
    path('', MatchListView.as_view(), name='match-list'),
]




# matches/utils.py に作成（共通処理として）

def create_match_if_mutual(from_user, to_user):
    # 順番を統一して格納
    user1, user2 = sorted([from_user, to_user], key=lambda x: x.id)

    # すでにマッチしていないかチェック
    if Match.objects.filter(user1=user1, user2=user2).exists():
        return  # すでにマッチ済み

    # 相手からのLikeがあるか確認
    if Like.objects.filter(from_user=to_user, to_user=from_user).exists():
        Match.objects.create(user1=user1, user2=user2)
        print(f"✅ Match作成: {user1.username} ❤️ {user2.username}")




from django.urls import path
from .views import MatchListView

urlpatterns = [
    path('', MatchListView.as_view(), name='match-list'),
]
