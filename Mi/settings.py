import os
import dj_database_url
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(^%g*p-nkttq=z=l(a3ws_i4$3qop*yi+d0hr*g_vf@f$j^ml='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django.contrib.postgres', #Added as it gave error to store data in db without this
    'corsheaders',
    'django.contrib.gis',
    'django_user_agents',

    #Self Made
    'socialmediaAuthentica',
    'CompilerApi',
    'PersonalNotes',
    'Users',
    'Friends',
    'Shared',
    'Notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
]

ROOT_URLCONF = 'Mi.urls'

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

WSGI_APPLICATION = 'Mi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         #'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'ENGINE': 'django.contrib.gis.db.backends.postgis',
#         'NAME': 'db11',
#         'USER': 'postgres',
#         'PASSWORD': 'abhi629@@',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }



DATABASES = {
    'default': dj_database_url.config(
        default=dj_database_url.config('postgres://xkwomrmbgqvczp:f9ae8151eb283ea46beff8d917a09870fb25214dd8dd120c7dda8607a9a310af@ec2-54-221-238-248.compute-1.amazonaws.com:5432/dch3oggdm23n00')
    )
}

DATABASES['default']['ENGINE'] = 'django.contrib.gis.db.backends.postgis'

GEOS_LIBRARY_PATH = '/app/.heroku/vendor/lib/libgeos_c.so' if os.environ.get('ENV') == 'HEROKU' else os.getenv('GEOS_LIBRARY_PATH')
GDAL_LIBRARY_PATH = '/app/.heroku/vendor/lib/libgdal.so' if os.environ.get('ENV') == 'HEROKU' else os.getenv('GDAL_LIBRARY_PATH')

# DATABASES = {
#      'default': dj_database_url.config(
#          default=dj_database_url.config('DATABASE_URL')
#      )
# }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
     'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
     ),
     'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER="abhinavshar657@gmail.com"
EMAIL_HOST_PASSWORD = 'hydra629@@'
EMAIL_PORT = 587


CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8001",
    "https://obscure-bayou-10492.herokuapp.com"
]


#JWT AUTHENTICATION SETTINGS
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),  #APIs authenticated using a JWT key, with validity of access_token = 5 days (can be manupulated according to need)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30), #APIs authenticated using a JWT key, with validity of refresh_token = 5 days (can be manupulated according to need)
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=30),
}


# #GDAL PATH
# import os
# if os.name == 'nt':
#     import platform
#     OSGEO4W = r"C:\OSGeo4W"
#     if '64' in platform.architecture()[0]:
#         OSGEO4W += "64"
#     assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
#     os.environ['OSGEO4W_ROOT'] = OSGEO4W
#     os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
#     os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
#     os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']


USER_AGENTS_CACHE = None