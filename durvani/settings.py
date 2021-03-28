
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MONGO_URL = 'mongodb://localhost:27017/'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(85s-d@3bn0xe^xyvw_^38djr*(zvkq06(p!xr&!f5+a$!bb6$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'rest_framework',
    'authentication',
    'quizz',

    'blog',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',

    'django_extensions',
    'corsheaders'
]

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

ROOT_URLCONF = 'durvani.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates'),os.path.join(BASE_DIR,'authentication/templates'),
        os.path.join(BASE_DIR,'quizz/templates'),os.path.join(BASE_DIR,'blog/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # in application
                'quizz.context_processors.basket',
                # AllAuth
                 'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'durvani.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'djongo',
    'NAME': 'reactreduxnode',
    'USER': '',
    # 'PASSWORD': 'digital#2020$',
    'PASSWORD' : '',
    'HOST': 'localhost',
    'PORT': 27017,
    'AUTH_SOURCE': 'admin',
    #'AUTH_MECHANISM': 'SCRAM-SHA-1'
    },
    'postgre': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'reactreduxnode',

        'USER': 'postgres',

        'PASSWORD': '9700416787n',

        'HOST': 'localhost',

        'PORT': 5432

    }
}


# Authentication Backends
# AUTHENTICATION_BACKENDS = (
    
#     # Needed to login by username in Django admin, regardless of `allauth`
#     'django.contrib.auth.backends.ModelBackend',

#     # `allauth` specific authentication methods, such as login by e-mail
#     # 'allauth.account.auth_backends.AuthenticationBackend',
    
# )
# CSRF_COOKIE_SECURE = False
CSRF_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = True

CORS_ORIGIN_ALLOW_ALL = True
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]

# X_FRAME_OPTIONS = 'SAMEORIGIN'
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": 
    [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
        # "rest_framework.permissions.AllowAny"
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'rest_framework.authentication.BasicAuthentication',
    #     # 'rest_framework_simplejwt.authentication.JWTAuthentication',
    #     'rest_framework.authentication.SessionAuthentication',
    #     # 'rest_framework.authentication.TokenAuthentication',
    # ),
    }


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8000",
]


CORS_ALLOW_CREDENTIALS = True

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Kolkata'


USE_I18N = True

USE_L10N = True

USE_TZ = True
# Smtp Setup

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'nagendrakumar422@gmail.com'
EMAIL_HOST_PASSWORD = 'hfhbijolsbordwmk'
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static/static_cdn/build/static'),
    os.path.join(BASE_DIR,'quizz/static'),
    
  
]







SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },
    'github': {
        'SCOPE': [
            'user',
            'repo',
            'read:org',
        ],
    },
    
}


SITE_ID = 1
LOGIN_REDIRECT_URL = '/admin'
SOCIALACCOUNT_AUTO_SIGNUP = True


GRAPH_MODELS = {
    'all_applications':True,
    'group_models':True
}