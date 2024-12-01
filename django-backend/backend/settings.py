"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_USER_MODEL = "api.CustomUser"

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.CustomTokenAuthentication',  # CustomToken 모델 사용
        'api.authentication.DebugTokenAuthentication',
        #'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # 인증 필요
    ],
}

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-yhsjrqah#cv8@s=2oa5_7#g(0s_wqh9&0iwosr@y)!-9(e7s(c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 추가 앱
    'rest_framework',
    # 커스텀 앱
    'api',  # api 디렉토리
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # 보안 미들웨어
    'corsheaders.middleware.CorsMiddleware',          # CORS 미들웨어
    'django.contrib.sessions.middleware.SessionMiddleware',  # 세션 미들웨어 (MessageMiddleware보다 위에 있어야 함)
    'django.middleware.common.CommonMiddleware',       # 일반 요청 미들웨어
    'django.middleware.csrf.CsrfViewMiddleware',       # CSRF 미들웨어
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # 인증 미들웨어
    'django.contrib.messages.middleware.MessageMiddleware',  # 메시지 미들웨어 (세션 미들웨어 뒤에)
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # 클릭재킹 방지
]


ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, '../coin-flip-game/build')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

INSTALLED_APPS += ['corsheaders',]

CORS_ORIGIN_ALLOW_ALL = True  # 모든 도메인 허용
CORS_ALLOW_ALL_ORIGINS = True


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # MySQL 데이터베이스 엔진
        'NAME': 'dbp',                   # 데이터베이스 이름
        'USER': 'dbproj',            # 사용자 이름 (Azure 형식으로 @hostname 포함)
        'PASSWORD': 'Projdb12',               # 사용자 비밀번호
        'HOST': 'dbdesign.mysql.database.azure.com',  # Azure SQL 호스트 이름
        'PORT': '3306',                       # MySQL 기본 포트
        'OPTIONS': {
            'ssl': {'ssl-mode': 'require'},   # SSL 모드 활성화
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'build/static'),  # React 정적 파일 경로
]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Debugging and logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}