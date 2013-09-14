# -*- coding: utf-8 -*-
# типичный набор настроек для sancta проектов

import os
import platform

# PATH - путь к manage.py
PATH = os.path.abspath(os.path.dirname(__file__) + '/../')

DEBUG = platform.node() != 'sancta'
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True
SITE_ID = 1

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.abspath(os.path.join(PATH, '../', 'files', 'media'))

DIRECTORY = os.path.abspath(
    os.path.join(PATH, '../', 'files', 'upload')
)

STATIC_ROOT = os.path.abspath(
    os.path.join(PATH, '../', 'files', 'collected_static')
)

STATIC_URL = '/static/'

STATICFILES_DIRS = (MEDIA_ROOT,)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.core.context_processors.i18n',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages'
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

INSTALLED_APPS = (
    # веб сервер
    'gunicorn',
    # все то, что предоставляется
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.redirects',
    # миграции
    'south',
    # scss
    'djcompass',
    #robot
    'robots_txt',
    #favion
    'favicon',
    #sitemap
    'django.contrib.sitemaps'
)

COMPASS_INPUT = os.path.abspath(os.path.join(MEDIA_ROOT, 'scss'))
COMPASS_OUTPUT = os.path.abspath(os.path.join(MEDIA_ROOT, 'css'))
COMPASS_STYLE = 'compressed'

FAVICONPATH = STATIC_URL + 'img/favicon.ico'

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

#
#
#    url(r'', include('robots_txt.urls')),
#    url(r'^', include('favicon.urls')),
#    url(r'^admin/', include(admin.site.urls)),
#
#
