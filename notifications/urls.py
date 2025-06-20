# notifications/urls.py

from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),  # GET /api/notifications/
]







from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.NotificationListView.as_view(), name='list'),
    path('<int:pk>/read/', views.MarkAsReadView.as_view(), name='mark-as-read'),  # ← 追加！
]



from matches.models import Match
from tracks.models import Like
from notifications.models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

def create_match_if_mutual(from_user, to_user):
    user1, user2 = sorted([from_user, to_user], key=lambda x: x.id)

    if Match.objects.filter(user1=user1, user2=user2).exists():
        return

    if Like.objects.filter(from_user=to_user, to_user=from_user).exists():
        # ✅ Match 作成
        Match.objects.create(user1=user1, user2=user2)

        # ✅ 通知を両方に送る
        Notification.objects.bulk_create([
            Notification(
                to_user=user1,
                message=f"{user2.username} さんとマッチしました！"
            ),
            Notification(
                to_user=user2,
                message=f"{user1.username} さんとマッチしました！"
            )
        ])

        print(f"🎉 Match created & notifications sent: {user1.username} ❤️ {user2.username}")




# notifications/urls.py

from django.urls import path
from .views import NotificationListView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
]
