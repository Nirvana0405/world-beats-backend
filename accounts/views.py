from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.core.signing import dumps, loads, BadSignature, SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from .models import CustomUser, Profile
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    ProfileSerializer,
)

User = get_user_model()


# ✅ ユーザー登録（仮登録＋メール送信）
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = False
        user.save()

        token = dumps(user.username)
        activation_url = f"{settings.FRONTEND_URL}/activate/{token}/"
        send_mail(
            subject="アカウント有効化リンク",
            message=f"以下のリンクをクリックしてアカウントを有効化してください:\n{activation_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )


# ✅ アカウント有効化
def activate_user(request, token):
    try:
        username = loads(token, max_age=60 * 60 * 24)  # 24時間有効
        user = User.objects.get(username=username)
        if not user.is_active:
            user.is_active = True
            user.save()
            return HttpResponse("アカウントが有効化されました！")
        return HttpResponse("すでに有効化済みのアカウントです。")
    except (User.DoesNotExist, BadSignature, SignatureExpired):
        return HttpResponse("無効なリンク、またはリンクの有効期限が切れています。", status=400)


# ✅ 基本情報（User）
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        # PATCH でプロフィール更新（Favorite genres など）
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ プロフィール詳細（主に画像などMultipart用）
class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ HTMLフォームベースの簡易ログイン（開発用）
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        return HttpResponse("ログイン成功")
