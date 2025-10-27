from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import Category

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    """
    Cria categorias padrão automaticamente quando um novo usuário é criado.
    """
    if created:
        # Categorias de INCOME (Entrada)
        income_categories = [
            {'name': 'Salário', 'color': '#10b981'},
            {'name': 'Freelance', 'color': '#059669'},
            {'name': 'Investimentos', 'color': '#34d399'},
            {'name': 'Outros Ganhos', 'color': '#6ee7b7'},
        ]

        # Categorias de EXPENSE (Saída)
        expense_categories = [
            {'name': 'Alimentação', 'color': '#ef4444'},
            {'name': 'Transporte', 'color': '#f59e0b'},
            {'name': 'Moradia', 'color': '#8b5cf6'},
            {'name': 'Saúde', 'color': '#ec4899'},
            {'name': 'Educação', 'color': '#3b82f6'},
            {'name': 'Lazer', 'color': '#14b8a6'},
            {'name': 'Compras', 'color': '#f97316'},
            {'name': 'Contas', 'color': '#6366f1'},
            {'name': 'Outros Gastos', 'color': '#64748b'},
        ]

        # Criar categorias de receita
        for category_data in income_categories:
            Category.objects.create(
                user=instance,
                name=category_data['name'],
                category_type=Category.INCOME,
                color=category_data['color']
            )

        # Criar categorias de despesa
        for category_data in expense_categories:
            Category.objects.create(
                user=instance,
                name=category_data['name'],
                category_type=Category.EXPENSE,
                color=category_data['color']
            )
