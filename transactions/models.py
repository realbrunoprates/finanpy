# Standard library
from decimal import Decimal

# Django imports
from django.core.validators import MinValueValidator
from django.db import models

# Local imports
from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    """
    Modelo para transações financeiras (receitas e despesas).

    Cada transação está vinculada a uma conta e uma categoria,
    e afeta o saldo da conta relacionada.
    """

    # Transaction type choices
    INCOME = 'income'
    EXPENSE = 'expense'

    TRANSACTION_TYPE_CHOICES = [
        (INCOME, 'Entrada'),
        (EXPENSE, 'Saída'),
    ]

    # Foreign Keys
    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Conta'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Categoria'
    )

    # Main fields
    transaction_type = models.CharField(
        'Tipo de Transação',
        max_length=10,
        choices=TRANSACTION_TYPE_CHOICES
    )

    amount = models.DecimalField(
        'Valor',
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    transaction_date = models.DateField('Data da Transação')

    description = models.TextField(
        'Descrição',
        blank=True
    )

    # MANDATORY timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['-transaction_date', '-created_at']
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        indexes = [
            models.Index(fields=['-transaction_date']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return f'{self.transaction_type} - {self.amount} - {self.transaction_date}'
