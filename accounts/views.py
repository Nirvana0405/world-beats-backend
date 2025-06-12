# ===========================
# 📦 標準ライブラリ
# ===========================
from django.core.mail import send_mail
from django.core.signing import dumps, loads, BadSignature, SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

# ===========================
# 🔧 Django / DRF
# ===========================
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

# ===========================
# 🏗️ アプリケーション
# ===========================
from .models import Profile
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileSerializer,
    PublicProfileSerializer,
)

User = get_user_model()
ACTIVATION_TOKEN_EXPIRY = 60 * 60 * 24  # 24時間（秒）

# ===========================
# 🔐 仮登録＋メール送信
# ===========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = dumps(user.username)
        activation_url = f"{settings.FRONTEND_URL}/activate/{token}/"

        # 🔔 ログ出力（開発用）
        print("🔗 アクティベーションリンク:", activation_url)

        send_mail(
            subject="アカウント有効化リンク",
            message=f"以下のリンクをクリックしてアカウントを有効化してください:\n{activation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

# ===========================
# ✅ アクティベーション処理
# ===========================
def activate_user(request, token):
    try:
        username = loads(token, max_age=ACTIVATION_TOKEN_EXPIRY)
        user = User.objects.get(username=username)
        if not user.is_active:
            user.is_active = True
            user.save()
            return HttpResponse("✅ アカウントが有効化されました！")
        return HttpResponse("⚠️ すでに有効化済みです。")
    except (User.DoesNotExist, BadSignature, SignatureExpired):
        return HttpResponse("❌ 無効または期限切れのリンクです。", status=400)

# ===========================
# 🔍 プロフィール取得/更新
# ===========================
def get_or_create_profile(user):
    return Profile.objects.get_or_create(user=user)[0]

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        profile = get_or_create_profile(request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

# ===========================
# 🖼️ プロフィール画像対応
# ===========================
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile = get_or_create_profile(request.user)
        return Response(ProfileSerializer(profile).data)

    def put(self, request):
        profile = get_or_create_profile(request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "画像を更新しました"})
        return Response(serializer.errors, status=400)

# ===========================
# 🧪 テスト用ログインページ
# ===========================
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        return HttpResponse("ログイン成功")

# ===========================
# ❌ アカウント論理削除
# ===========================
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({"message": "アカウントを削除しました。"}, status=204)

# ===========================
# 🌐 他人プロフィール公開用
# ===========================
class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        return Response(PublicProfileSerializer(profile).data)
