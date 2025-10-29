from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    """Configurações da aplicação de perfis de usuário."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'profiles'

    def ready(self):
        """Importa os signals de perfil durante a inicialização."""
        import profiles.signals  # noqa: F401
