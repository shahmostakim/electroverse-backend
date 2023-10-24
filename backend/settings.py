
from pathlib import Path
import os 

from decouple import config 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# cleans and returns a list of allowed hosts 
def getAllowedHostsCleaned(rawValue): 
    allowedHosts = [] 
    for item in rawValue.split(','): 
        allowedHosts.append(item.strip())
    return allowedHosts


try: 
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    #ALLOWED_HOSTS = []
    # fetchs the value and transforms into a list using lambda function by comma separating 
    # the values and then cleaning up whitespaces  
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='', cast=lambda v: [s.strip() for s in v.split(',')])
except: 
    SECRET_KEY = os.environ.get('SECRET_KEY')
    DEBUG = os.environ.get('DEBUG')
    #ALLOWED_HOSTS_RAW = os.environ.get('ALLOWED_HOSTS')
    #ALLOWED_HOSTS = getAllowedHostsCleaned(ALLOWED_HOSTS_RAW)
    ALLOWED_HOSTS = ['18.222.169.81']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'api.apps.ApiConfig',  
    'rest_framework', 
    'corsheaders',
    'storages', 
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    #"SIGNING_KEY": settings.SECRET_KEY,
    "VERIFYING_KEY": "", 
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            #os.path.join(BASE_DIR, '..', 'frontend/build') 
        ],
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

# default local sqlite database, for remote database settings, refer to bottom section 
# this DB settings is not being used 
DATABASES_LOCAL = {
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# ========= settings for uploaded media files ===================
STATICFILES_DIRS = [
    #BASE_DIR / 'static',
    #os.path.join(BASE_DIR, 'static'), 
    #os.path.join(BASE_DIR, '..', 'frontend/build/static'), 
]

#MEDIA_ROOT = 'static/images' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'static', 'images')
MEDIA_URL = 'images/'
# =================================================================

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# allows api requests from any origin 
CORS_ALLOW_ALL_ORIGINS = True 

'''
# load secret settings (inactive now)
try: 
    from .secrets import DBCONFIG, MEDIA_FILE_STORAGE, KEY_ID, MY_ACCESS_KEY, BUCKET_NAME
except ImportError: 
    DBCONFIG = DATABASES_LOCAL

#remote  database 
DATABASES = DBCONFIG 
'''


# remote media file storage using secrets.py  
#DEFAULT_FILE_STORAGE = MEDIA_FILE_STORAGE 
#AWS_ACCESS_KEY_ID = KEY_ID
#AWS_SECRET_ACCESS_KEY = MY_ACCESS_KEY 
#AWS_STORAGE_BUCKET_NAME = BUCKET_NAME  
AWS_DEFAULT_ACL = None 
AWS_S3_FILE_OVERWRITE = True   
AWS_QUERYSTRING_AUTH = False 


try: 
    # remote media file storage using env variables 
    DEFAULT_FILE_STORAGE = config('MEDIA_FILE_STORAGE')
    AWS_ACCESS_KEY_ID = config('KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('MY_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('BUCKET_NAME')
except:
    DEFAULT_FILE_STORAGE = os.environ.get('MEDIA_FILE_STORAGE')
    AWS_ACCESS_KEY_ID = os.environ.get('KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('MY_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.environ.get('BUCKET_NAME')


try: 
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT'),
        }
    } 
except: 
    DATABASES = {
        'default': {
            'ENGINE': os.environ.get('DB_ENGINE'),
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT'),
        }
    } 

# Deployment settings 
'''
# HTTPS settings 
SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True 
SECURE_SSL_REDIRECT = True 

# HSTS settings 
SECURE_HSTS_SECONDS = 31536000 # 1 year 
SECURE_HSTS_PRELOAD = True 
SECURE_HSTS_INCLUDE_SUBDOMAINS = True 
'''
