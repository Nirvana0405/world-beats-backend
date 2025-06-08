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
