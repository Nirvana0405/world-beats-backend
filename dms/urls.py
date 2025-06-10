# dms/urls.py

from django.urls import path
from .views import (
    DirectMessageListCreateView,
    dm_thread_list,
    dm_thread_detail,
)

urlpatterns = [
    # 📩 1対1 DM の送受信
    path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),

    # 🧵 DMスレッドの一覧（相手ごとに最新メッセージ＋未読数）
    path('threads/', dm_thread_list, name='dm-thread-list'),

    # 💬 スレッド詳細（指定した相手との全履歴）
    path('threads/<int:user_id>/', dm_thread_detail, name='dm-thread-detail'),
]






# dms/urls.py
from django.urls import path
from .views import (
    DirectMessageListCreateView,
    dm_thread_list,
    dm_thread_detail,
)

urlpatterns = [
    path('threads/', dm_thread_list, name='dm-thread-list'),
    path('threads/<int:user_id>/', dm_thread_detail, name='dm-thread-detail'),
    path('direct-messages/', DirectMessageListCreateView.as_view(), name='direct-message-list-create'),
]
