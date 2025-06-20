# dms/urls.py

from django.urls import path
from .views import (
    DirectMessageListCreateView,
    dm_thread_list,
    dm_thread_detail,
)

urlpatterns = [
    # 🧵 スレッド一覧（相手ごとの最新メッセージ＋未読数）
    path('threads/', dm_thread_list, name='dm-thread-list'),

    # 💬 スレッド詳細（特定ユーザーとの全DM履歴）
    path('threads/<int:user_id>/', dm_thread_detail, name='dm-thread-detail'),

    # 📩 1対1のメッセージ送信・一覧（Postで送信）
    path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
]
