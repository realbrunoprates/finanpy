from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configurações da aplicação de contas bancárias."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
