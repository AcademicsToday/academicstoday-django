"""
Django settings for academicstoday_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o6$v5vhh(r=a*0dkl^)5)%x1wyb6tjzo-8@76lqb*b6lheos&m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'landpage',
    'registrar',
    'course'
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

ROOT_URLCONF = 'academicstoday_project.urls'

WSGI_APPLICATION = 'academicstoday_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "academicstoday_db",
        "USER": "bart",
        "PASSWORD": "123password",
        "HOST": "localhost",
        "PORT": "5432",
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

# ( See: http://en.wikipedia.org/wiki/List_of_tz_database_time_zones )
TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)


# User uploaded content.
#

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Custom Constants
#

# Question Types
ESSAY_ASSIGNMENT_TYPE = 1
MULTIPLECHOICE_ASSIGNMENT_TYPE = 2
TRUEFALSE_ASSIGNMENT_TYPE = 3
RESPONSE_ASSIGNMENT_TYPE = 4

# Course Status
COURSE_UNAVAILABLE_STATUS = 0
COURSE_AVAILABLE_STATUS = 1

# JavaScript Libraries
#
SB_ADMIN_CSS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery-ui.css",
    "js/bootstrap/3.3.2/css/bootstrap.min.css",
    "js/font-awesome/4.2.0/css/font-awesome.css",
    "js/font-awesome/4.2.0/css/font-awesome.min.css",
    "css/sb-admin.css"
]

SB_ADMIN_JS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery.min.js",
    "js/jquery/1.11.1/jquery.tablesorter.js",
    "js/jquery/1.11.1/jquery-ui.js",
    "js/jquery-easing/1.3/jquery.easing.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.js",
#     "js/morris/0.5.0/morris.js",
#     "js/morris/0.5.0/morris.min.js",
    "js/morris/0.5.0/raphael.min.js",
#    "js/morris/0.5.0/morris-data.js",
#    "js/flot/x.x/excanvas.min.js",
#    "js/flot/x.x/flot-data.js",
#    "js/flot/x.x/jquery.flot.js",
#    "js/flot/x.x/jquery.flot.pie.js",
#    "js/flot/x.x/jquery.flot.resize.js",
#    "js/flot/x.x/jquery.flot.tooltip.min.js",
]

AGENCY_CSS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery-ui.css",
    "js/bootstrap/3.3.2/css/bootstrap.min.css",
    "js/font-awesome/4.2.0/css/font-awesome.css",
    "js/font-awesome/4.2.0/css/font-awesome.min.css",
    "css/landpage.css",
    "css/agency.css"
]

AGENCY_JS_LIBRARY_URLS = [
    "js/jquery/1.11.1/jquery.min.js",
    "js/jquery/1.11.1/jquery.tablesorter.js",
    "js/jquery/1.11.1/jquery-ui.js",
    "js/jquery-easing/1.3/jquery.easing.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.min.js",
    "js/bootstrap/3.3.2/js/bootstrap.js",
    "js/classie/1.0.0/classie.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.js",
    "js/cbpanimatedheader/1.0.0/cbpAnimatedHeader.min.js",
    "js/jqbootstrapvalidation/1.3.6/jqBootstrapValidation.js",
    "js/misc/agency.js"
]
