from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Account(models.Model):
    """
    Representa uma conta bancária ou carteira do usuário.
    Pode ser conta corrente, poupança ou carteira física.
    """

    # Account type choices
    CHECKING = 'checking'
    SAVINGS = 'savings'
    WALLET = 'wallet'

    ACCOUNT_TYPE_CHOICES = [
        (CHECKING, 'Conta Corrente'),
        (SAVINGS, 'Poupança'),
        (WALLET, 'Carteira'),
    ]

    # Foreign Keys
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuário'
    )

    # Main fields
    name = models.CharField('Nome', max_length=100)
    bank_name = models.CharField('Banco', max_length=100)
    account_type = models.CharField(
        'Tipo de Conta',
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=CHECKING
    )
    balance = models.DecimalField(
        'Saldo',
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(Decimal('0'))]
    )

    # Status
    is_active = models.BooleanField('Ativo', default=True)

    # Timestamps
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        indexes = [
            models.Index(fields=['user', 'is_active']),
        ]

    def __str__(self):
        return self.name
