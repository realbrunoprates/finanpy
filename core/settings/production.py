import dj_database_url
from decouple import Csv, config

from .base import *  # noqa: F401,F403


DEBUG = config('DEBUG', default=False, cast=bool)

ENVIRONMENT = 'production'
IS_PRODUCTION = True

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='',
    cast=Csv(),
)

if not ALLOWED_HOSTS:
    raise ValueError(
        'ALLOWED_HOSTS must be configured for production environments.',
    )

database_url = config('DATABASE_URL', default=None)
if database_url:
    DATABASES['default'] = dj_database_url.parse(
        database_url,
        conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
        ssl_require=config('DB_SSL_REQUIRE', default=True, cast=bool),
    )

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': (
            'whitenoise.storage.CompressedManifestStaticFilesStorage'
        ),
    },
}

SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
SECURE_HSTS_SECONDS = config(
    'SECURE_HSTS_SECONDS',
    default=31536000,
    cast=int,
)
