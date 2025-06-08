# matches/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .models import UserLike
from .serializers import MatchUserSerializer

User = get_user_model()

class MatchListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 自分がLikeしたユーザーID
        liked_users = UserLike.objects.filter(from_user=user).values_list('to_user', flat=True)

        # 自分をLikeしてくれたユーザーID
        liked_by_users = UserLike.objects.filter(to_user=user).values_list('from_user', flat=True)

        # 両方がLikeした（マッチした）ユーザーID
        matched_user_ids = set(liked_users).intersection(liked_by_users)

        # マッチしたユーザー一覧を取得
        matched_users = User.objects.filter(id__in=matched_user_ids)
        serializer = MatchUserSerializer(matched_users, many=True)

        return Response(serializer.data)





from notifications.models import Notification

class MatchCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user1 = request.user
        user2_id = request.data.get("target_user_id")
        user2 = User.objects.get(id=user2_id)

        # すでに相互Likeされてるかチェック（省略可）

        # ✅ マッチ作成（例）
        match = Match.objects.create(user1=user1, user2=user2)

        # ✅ お互いに通知作成
        Notification.objects.create(
            to_user=user1,
            message=f"{user2.username} さんとマッチしました！"
        )
        Notification.objects.create(
            to_user=user2,
            message=f"{user1.username} さんとマッチしました！"
        )

        return Response({"detail": "Match created!"}, status=201)
