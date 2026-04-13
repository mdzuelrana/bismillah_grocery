from pathlib import Path
from datetime import timedelta
import dj_database_url
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Security ──────────────────────────────────────────────────────────────────
SECRET_KEY = os.environ.get("SECRET_KEY")   # ✅ move to .env
DEBUG       = os.environ.get("DEBUG", "False") == "True"
ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'users.User'

# ── Apps ──────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",
    'django.contrib.staticfiles',
    'drf_yasg',
    'users',
    'tasks',
    'order',
    'cart',
    'review',
    'payments',
    "corsheaders",
    'rest_framework',
    'djoser',
]

# ── Middleware ─────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── DRF ───────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # global default
        # payment success/fail/cancel views override this with AllowAny
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME":  timedelta(days=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# ── Database ──────────────────────────────────────────────────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# ── Cache ─────────────────────────────────────────────────────────────────────
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",  # ✅ fixes cached_db session error
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.db"  # ✅ simpler — no cache needed

# ── Templates ─────────────────────────────────────────────────────────────────
ROOT_URLCONF    = 'grocery.urls'
WSGI_APPLICATION = 'grocery.wsgi.app'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_APPS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── Password validation ───────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ── Internationalisation ──────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE      = 'Asia/Dhaka'   # ✅ set to Bangladesh timezone
USE_I18N = True
USE_TZ   = True

# ── CORS & CSRF ───────────────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True
CSRF_TRUSTED_ORIGINS = [
    "https://bismillah-grocery.vercel.app",
    "https://grocery-frontend-nine.vercel.app",
    "https://sandbox.sslcommerz.com",   # ✅ trust SSLCommerz for CSRF
]

# ── Static & Media ────────────────────────────────────────────────────────────
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"
STATIC_URL  = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL   = '/media/'
MEDIA_ROOT  = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ── Djoser ────────────────────────────────────────────────────────────────────
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL':             'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL':      True,
    'LOGIN_FIELD':                'username',
    'USER_CREATE_PASSWORD_RETYPE': True,
    'SERIALIZERS': {
        'user_create':    'users.serializers.CustomUserCreateSerializer',
        'user':           'users.serializers.ProfileSerializer',
        'current_user':   'users.serializers.ProfileSerializer',
    },
}

# ── Swagger ───────────────────────────────────────────────────────────────────
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type':        'apiKey',
            'name':        'Authorization',
            'in':          'header',
            'description': 'Enter your JWT token as: Bearer <token>',
        }
    }
}

# ── Email ─────────────────────────────────────────────────────────────────────
EMAIL_BACKEND       = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST          = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_USE_TLS       = True
EMAIL_HOST_USER     = os.environ.get("EMAIL_HOST_USER")      # ✅ move to .env
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")  # ✅ move to .env
DEFAULT_FROM_EMAIL  = os.environ.get("EMAIL_HOST_USER")

# ── SSLCommerz ────────────────────────────────────────────────────────────────
SSLCOMMERZ_STORE_ID       = os.environ.get("SSLCOMMERZ_STORE_ID", "testbox")
SSLCOMMERZ_STORE_PASSWORD = os.environ.get("SSLCOMMERZ_STORE_PASSWORD", "qwerty")
SSLCOMMERZ_INIT_URL       = "https://sandbox.sslcommerz.com/gwprocess/v4/api.php"
SSLCOMMERZ_VALIDATION_URL = "https://sandbox.sslcommerz.com/validator/api/validationserverAPI.php"

# ── URLs ──────────────────────────────────────────────────────────────────────
BASE_URL     = os.environ.get("BASE_URL",     "https://bismillah-grocery.vercel.app")
FRONTEND_URL = os.environ.get("FRONTEND_URL", "https://grocery-frontend-nine.vercel.app")