from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Configurações da aplicação responsável por usuários personalizados."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
