# accounts/views.py

# ===========================
# 📆 標準ライブラリ
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
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

# ===========================
# 📆 アプリケーション
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
# 📩 ユーザー登録 + メール送信
# ===========================
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        token = dumps(user.username)
        activation_url = f"{settings.FRONTEND_URL}/activate/{token}/"

        print("🔗 アクティベーションリンク:", activation_url)

        send_mail(
            subject="アカウント有効化リンク",
            message=f"以下のリンクをクリックしてアカウントを有効化してください:\n{activation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

# ===========================
# ✅ アクティベーション
# ===========================
class ActivateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            username = loads(token, max_age=ACTIVATION_TOKEN_EXPIRY)
            user = User.objects.get(username=username)

            if user.is_active:
                return Response({"detail": "⚠️ このアカウントはすでに有効化されています。"}, status=200)

            user.is_active = True
            user.save()
            return Response({"detail": "✅ アカウントが有効化されました！"}, status=200)

        except SignatureExpired:
            return Response({"detail": "❌ リンクの有効期限が切れています。"}, status=400)

        except (BadSignature, User.DoesNotExist):
            return Response({"detail": "❌ 無効なリンクです。"}, status=400)

# ===========================
# 👤 プロフィール
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
# 🚪 ログイン画面
# ===========================
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        return HttpResponse("ログイン成功")

# ===========================
# ❌ アカウント削除
# ===========================
class DeactivateAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        request.user.is_active = False
        request.user.save()
        return Response({"message": "アカウントを削除しました。"}, status=204)

# ===========================
# 🌍 他人プロフィール
# ===========================
class PublicProfileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, user_id):
        profile = get_object_or_404(Profile, user__id=user_id)
        return Response(PublicProfileSerializer(profile).data)
