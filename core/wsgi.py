"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.getenv('ENVIRONMENT', 'production').lower()
settings_map = {
    'production': 'core.settings.production',
    'development': 'core.settings.development',
}
default_settings = settings_map.get(environment, 'core.settings.production')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)

application = get_wsgi_application()
