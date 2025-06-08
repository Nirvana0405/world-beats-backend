from pathlib import Path
import os
import json


# 📁 ベースディレクトリ
BASE_DIR = Path(__file__).resolve().parent.parent

# 🔐 セキュリティキー（開発用）
SECRET_KEY = 'django-insecure-ih=v1z(#pjpn+1=dk8s0%zkm$)g*pc#5*!_3l6gmly$fu$8_m+'

# ⚠️ 本番環境では必ず False に
DEBUG = True

#ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'yourdomain.com']
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'world-beats-backend.onrender.com']


# 🧩 アプリケーション定義
INSTALLED_APPS = [
    # Django 標準
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 外部パッケージ
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',

    # 自作アプリ
    'accounts',
    'tracks',
    'profiles',
    'myapp',
    'matches',
    'dms',
    'notifications',
]

# 🌐 ミドルウェア
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 必ず先頭に
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ルーティング
ROOT_URLCONF = 'config.urls'

# テンプレート設定
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

# WSGI アプリ
WSGI_APPLICATION = 'config.wsgi.application'

# 🗄️ データベース設定（SQLite）
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 🔐 パスワードバリデーション
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# 🌍 国際化
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# 📁 静的・メディアファイル
STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ カスタムユーザーモデル
AUTH_USER_MODEL = 'accounts.CustomUser'

# 🔐 JWT 認証設定
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# 📧 メール設定（開発用）
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'noreply@example.com'

# 🔗 Next.js 連携
FRONTEND_URL = 'http://localhost:3000'

# 🔓 CORS 許可設定（開発用）
CORS_ALLOW_ALL_ORIGINS = True
# 本番用：
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://your-frontend.com",
# ]

# 🔧 主キー自動設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



import os
import dj_database_url

DEBUG = os.getenv("DEBUG", "False") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-key")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

CORS_ALLOWED_ORIGINS = json.loads(os.getenv("CORS_ALLOWED_ORIGINS", "[]"))

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}
