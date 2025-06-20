from django.urls import path
from .views import (
    ProfileRetrieveUpdateView,     # /api/profiles/me/
    PublicProfileDetailView,       # /api/profiles/<user_id>/
    OtherUserProfilesView,         # /api/profiles/others/
    PublicProfileListView          # /api/profiles/（検索など）
)

urlpatterns = [
    # ✅ 自分のプロフィール（取得・更新）
    path("me/", ProfileRetrieveUpdateView.as_view(), name="my-profile"),

    # 👥 他人プロフィールの一覧（自分を除外）
    path("others/", OtherUserProfilesView.as_view(), name="other-profiles"),

    # 🔍 全公開プロフィール一覧（検索対応）
    path("", PublicProfileListView.as_view(), name="public-profile-list"),

    # 👁 他人のプロフィール詳細（指定ID）
    path("<int:user_id>/", PublicProfileDetailView.as_view(), name="public-profile-detail"),
]
