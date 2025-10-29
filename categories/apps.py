from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """Configurações da aplicação de categorias financeiras."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'categories'

    def ready(self):
        """
        Import signals when Django starts.
        """
        import categories.signals
