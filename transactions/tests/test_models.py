from decimal import Decimal
from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class TestTransactionModel(TestCase):
    """Tests for the Transaction model behaviour and validations."""

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='transaction@example.com',
            password='safe-pass'
        )
        self.account = Account.objects.create(
            user=self.user,
            name='Conta Teste',
            bank_name='Banco Teste'
        )
        self.category = self.user.categories.get(name='Salário')

    def test_transaction_str_representation(self):
        """__str__ must include type, amount and date."""
        transaction = Transaction.objects.create(
            account=self.account,
            category=self.category,
            transaction_type=Transaction.INCOME,
            amount=Decimal('2500.00'),
            transaction_date=date(2024, 1, 15),
            description='Pagamento mensal'
        )

        self.assertEqual(
            str(transaction),
            'income - 2500.00 - 2024-01-15'
        )

    def test_transaction_amount_cannot_be_zero_or_negative(self):
        """Amount must be at least 0.01."""
        transaction = Transaction(
            account=self.account,
            category=self.category,
            transaction_type=Transaction.EXPENSE,
            amount=Decimal('0.00'),
            transaction_date=date(2024, 2, 10)
        )

        with self.assertRaises(ValidationError):
            transaction.full_clean()

    def test_invalid_transaction_type_raises_error(self):
        """Only valid choices for transaction_type are accepted."""
        transaction = Transaction(
            account=self.account,
            category=self.category,
            transaction_type='bonus',
            amount=Decimal('100.00'),
            transaction_date=date(2024, 3, 1)
        )

        with self.assertRaises(ValidationError):
            transaction.full_clean()
