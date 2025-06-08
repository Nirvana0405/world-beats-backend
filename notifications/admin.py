from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('to_user', 'message', 'is_read', 'created_at')  # ← 修正
    list_filter = ('is_read', 'created_at')                         # ← 修正
