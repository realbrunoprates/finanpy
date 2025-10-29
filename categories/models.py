from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    """
    Modelo de categorias de transações financeiras.
    Cada usuário pode criar suas próprias categorias de receita ou despesa.
    """
    # Choices para tipo de categoria
    INCOME = 'income'
    EXPENSE = 'expense'
    CATEGORY_TYPE_CHOICES = [
        (INCOME, 'Receita'),
        (EXPENSE, 'Despesa'),
    ]

    # Foreign Key
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Usuário'
    )

    # Main fields
    name = models.CharField('Nome', max_length=50)
    category_type = models.CharField(
        'Tipo',
        max_length=10,
        choices=CATEGORY_TYPE_CHOICES
    )
    color = models.CharField('Cor', max_length=7, default='#667eea')

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        """Controla ordenação, textos e restrições exclusivas das categorias."""

        ordering = ['name']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        indexes = [
            models.Index(fields=['user', 'category_type']),
        ]
        unique_together = [['user', 'name']]

    def __str__(self):
        return self.name
