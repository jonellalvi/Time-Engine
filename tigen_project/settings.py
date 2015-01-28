"""
Django settings for tigen_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# django is looking here:
# Django tried loading these templates, in this order:
#
#     Using loader django.template.loaders.filesystem.Loader:
#         C:\Jonell\Projects\apps\djangotest\tigen_project\templates\time_engine\index.html (File does not exist)
# Actual: C:\Jonell\Projects\apps\djangotest\tigen_project\templates\time_engine\index.html
#     Using loader django.template.loaders.app_directories.Loader:
#         C:\Jonell\Projects\apps\djangotest\venv\lib\site-packages\django\contrib\admin\templates\time_engine\index.html (File does not exist)
#         C:\Jonell\Projects\apps\djangotest\venv\lib\site-packages\django\contrib\auth\templates\time_engine\index.html (File does not exist)
#

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print BASE_DIR

PROJECT_PATH = os.path.join(BASE_DIR, os.pardir)
#PROJECT_PATH = os.path.join(PROJECT_PATH)
DATABASE_PATH = os.path.join(PROJECT_PATH, 'tigen_project', 'db.sqlite3')
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'tigen_project', 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_ciazhi-75z2=6rtg8&7oyx&8p=y(zv#7+3a43z72+d-(9avxu'
# Below is the old secret key from version 1.5.4 of time_gen project
#SECRET_KEY = '%$6ghy&!7+&z*074iff$04)d=r^t@%%)sisjdpiqy#7(ja6+!y'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'time_engine',
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

ROOT_URLCONF = 'tigen_project.urls'
# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tigen_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        #'NAME': DATABASE_PATH,
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Los_Angeles'
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True
# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = ''

STATIC_PATH = 'c:/Jonell/Projects/apps/djangotest/tigen_project/static' #os.path.join(PROJECT_PATH, 'static')
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    STATIC_PATH,
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    TEMPLATE_PATH,
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

#Password stuff:
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
