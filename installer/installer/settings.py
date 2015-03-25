import os
import dj_database_url
from configurations import Settings
from secret import DATABASE_SETTINGS


class Base(Settings):
    USER_NAME = os.environ.get('USER', '')
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'installer_profile',
        'installer_config',
        'django_jinja',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'installer.urls'
    WSGI_APPLICATION = 'installer.wsgi.application'

    DATABASES = {
            'default': dj_database_url.config(
                default='postgres://{}:@localhost:5432/installer'.format(USER_NAME))
                # default='postgres://postgres:admin@localhost:5432/installer_dbase')
        }

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Los_Angeles'

    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "installer/static/"),
        )

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, "installer/templates/"),
        )

    TEMPLATE_LOADERS = (
        'django_jinja.loaders.FileSystemLoader',
        'django_jinja.loaders.AppLoader',
    )

    DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.jinja2'

    ACCOUNT_ACTIVATION_DAYS = 7
    REGISTRATION_AUTO_LOGIN = True
    REGISTRATION_OPEN = True
    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/profile/'


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    SECRET_KEY = 'secret'


class Prod(Base):

    DATABASES = DATABASE_SETTINGS

    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    SECRET_KEY = os.environ.get('SECRET_KEY')
    ALLOWED_HOSTS = ['.ec2-54-149-69-177.us-west-2.compute.amazonaws.com']
