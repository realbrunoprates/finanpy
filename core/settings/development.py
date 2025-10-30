from .base import *  # noqa: F401,F403


DEBUG = True

ENVIRONMENT = 'development'
IS_PRODUCTION = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
