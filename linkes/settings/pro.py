from .base import *

DEBUG = False

ADMINS = (
    ('Matthew Coady', 'matthew@leehair.co.uk'),
)

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'linkes',
        'USER': 'linkes',
        # removed password
    }
}

CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
