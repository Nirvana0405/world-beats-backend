from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["username", "email", "is_staff"]

    # ⚠️ 新規ユーザー作成画面に email 入力欄を追加
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            None,
            {
                "fields": ("email",),
            },
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
