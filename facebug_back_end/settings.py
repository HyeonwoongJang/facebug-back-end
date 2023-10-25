"""
Django settings for facebug_back_end project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-x9f4&*0!s!az)q$bos#1h56@57#y6h1fs6#(_xq9jv!#!@d&4h'

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

    'corsheaders',

    'rest_framework',
    'rest_framework_simplejwt',

    'user',
    'post',
]

REST_FRAMEWORK = {

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'facebug_back_end.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'facebug_back_end.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DEFAULT_PROFILE_IMAGE = 'user/DefaultProfileImage.jpg'

AUTH_USER_MODEL = 'user.User'

# CORS_ALLOWED_ORIGINS = [

# ]

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_HOST = 'smtp.gmail.com' 		                # 메일 호스트 서버
EMAIL_PORT = 587 			                        # SMTP 포트 번호
EMAIL_HOST_USER = 'hyeonwoongjang01@gmail.com' 	    # 서비스에서 사용할 Gmail
EMAIL_HOST_PASSWORD = ''                            # 서비스에서 사용할 Gmail의 password

EMAIL_USE_TLS = True                                # 사용자의 이메일 서버와의 통신에 TLS(Transport Layer Security)를 사용하면 데이터를 암호화하여 안전한 통신을 보장합니다.
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CELERY_BROKER_URL = 'amqp://guest@localhost:5672//' # Celery와 같은 작업 대기열 시스템에서 작업을 비동기적으로 처리하기 위해 활용되는 메시지 브로커입니다.
                                                    # 정의한 url은 RabbitMQ 메시지 브로커 서버에 연결하는데 사용되는 URL입니다.
CELERY_RESULT_BACKEND = 'rpc://'                    # Celery 작업의 결과를 저장하는 백엔드 저장소를 설정하는 데 사용되는 환경 변수 또는 설정 옵션입니다. 이 설정은 Celery가 비동기 작업을 처리하고 작업의 결과를 저장하는 방법을 지정합니다.
                                                    # rpc://로 설정하면 작업 결과가 메시지 브로커에 저장되며 작업 수행자는 해당 결과를 검색합니다.
CELERY_RESULT_EXPIRES = 3600                        # 작업 결과를 설정된 시간(초) 동안 보관합니다.