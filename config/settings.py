import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# ===============================
# 🔧 環境変数の読み込み
# ===============================
load_dotenv()

# ===============================
# 📁 パス設定
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# 🔐 セキュリティ設定
# ===============================
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-dev-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

# ===============================
# 🔌 アプリケーション
# ===============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',

    'accounts',
    'tracks',
    'profiles',
    'myapp',
    'matches',
    'dms',
    'notifications',
]

# ===============================
# 🔧 ミドルウェア
# ===============================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ===============================
# 🔗 URL & WSGI
# ===============================
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'

# ===============================
# 🗄️ データベース
# ===============================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600
    )
}

# ===============================
# 🖼️ テンプレート
# ===============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ===============================
# 🔐 認証設定
# ===============================
AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# ===============================
# 🌍 国際化
# ===============================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True

# ===============================
# 📁 静的 & メディアファイル
# ===============================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ===============================
# 📧 メール設定
# ===============================
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@example.com")

# ===============================
# 🌐 フロントエンドURL
# ===============================
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

# ===============================
# 🔓 CORS 設定
# ===============================
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = [
    # 本番環境
    "https://world-beats-frontend-d5ix-jrd8jvlzm-nirvana0405s-projects.vercel.app",
    "https://world-beats-frontend-gkq8.vercel.app",

    # 過去のデプロイURL
    "https://world-beats-frontend-d5ix-evkpstd9m-nirvana0405s-projects.vercel.app",
    "https://world-beats-frontend-d5ix-40btfnxxz-nirvana0405s-projects.vercel.app",

    # ローカル開発
    "http://localhost:3000",
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
]

# ===============================
# 🔧 その他
# ===============================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
