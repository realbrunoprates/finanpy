from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    """Configurações da aplicação de transações financeiras."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
    verbose_name = 'Transações'

    def ready(self):
        """
        Importa os signals quando a aplicação está pronta.

        Este método é chamado pelo Django durante a inicialização da aplicação.
        Importamos os signals aqui para garantir que eles sejam registrados
        corretamente antes de qualquer operação no banco de dados.
        """
        import transactions.signals  # noqa: F401
