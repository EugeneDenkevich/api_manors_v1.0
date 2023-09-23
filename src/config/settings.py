try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import os

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'Admin123')

DEBUG = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

FRONTEND_URL = "http://zapovedny-front.eugenestudio.site/"

ALLOWED_HOSTS = ['http://localhost:3000', 'https://api.zapovedny.travelweb.dev']

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://zapovedny.travelweb.dev",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'object.apps.ObjectConfig',
    'entertainments.apps.EntertainmentsConfig',
    'info.apps.InfoConfig',
    'pages.apps.PagesConfig',
    'authentication.apps.AuthenticationConfig',
    
    # thrid side apps
    'corsheaders',
    'sorl.thumbnail',
    'rest_framework',
    'phonenumber_field',
    'drf_spectacular',
    'drf_spectacular_sidecar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
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

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.mysql',
    'OPTIONS': {
        'sql_mode': 'traditional',
        },
    'NAME': os.environ.get('MYSQL_DATABASE'),
    'USER': os.environ.get('MYSQL_USER'),
    'PASSWORD': os.environ.get('MYSQL_ROOT_PASSWORD'),
    'HOST': os.environ.get('MYSQL_DJANGO_HOST'),
    'PORT': os.environ.get('MYSQL_PORT'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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

LANGUAGE_CODE = 'ru'
# LANGUAGE_CODE = 'en'

TIME_ZONE = 'Europe/Moscow'
# TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = os.environ.get('STATIC_URL', '/src/static/')
STATIC_ROOT = os.environ.get('STATIC_ROOT', '/home/eugenest/WwW/zapovedny.travelweb.dev/api/repo/src/static/')
MEDIA_URL = os.environ.get('MEDIA_URL', '/src/media/')
MEDIA_ROOT = os.environ.get('MEDIA_ROOT', '/home/eugenest/WwW/zapovedny.travelweb.dev/api/repo/src/media/')

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'}
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',
            # 'level': 'DEBUG'
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'TIME_FORMAT': "%H:%M",
}

SPECTACULAR_SETTINGS = {
    'CONTACT': {
        'name': 'Eugene Denkevich',
        'email': 'eugenestudio@mail.ru'
    },
    'TITLE': 'Zapovedniy API',
    'DESCRIPTION': 'API for the website of manors owners',
    'SCHEMA_PATH_PREFIX': None,
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

MAX_IMAGE_SIZE_MB = 2.0
MAX_IMAGE_SIZE = MAX_IMAGE_SIZE_MB * (1024**2)

MAX_NUMBER_OF_GUESTS = 50

AUTH_USER_MODEL = 'authentication.BaseUser'