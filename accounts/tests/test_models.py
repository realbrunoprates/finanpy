from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.models import Account


class TestAccountModel(TestCase):
    """Tests for the Account model behaviour and validations."""

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='banker@example.com',
            password='safe-pass'
        )

    def test_account_str_returns_name(self):
        """__str__ must return the account name."""
        account = Account.objects.create(
            user=self.user,
            name='Conta Principal',
            bank_name='Banco Central',
            account_type=Account.CHECKING,
            balance=Decimal('1500.00')
        )

        self.assertEqual(str(account), 'Conta Principal')

    def test_account_has_expected_defaults(self):
        """Ensure account defaults are configured as expected."""
        account = Account.objects.create(
            user=self.user,
            name='Conta Poupança',
            bank_name='Banco Seguro'
        )

        self.assertEqual(account.account_type, Account.CHECKING)
        self.assertEqual(account.balance, Decimal('0.00'))
        self.assertTrue(account.is_active)

    def test_account_balance_cannot_be_negative(self):
        """Balance must respect the minimum value validator."""
        account = Account(
            user=self.user,
            name='Conta Inválida',
            bank_name='Banco Alert',
            balance=Decimal('-10.00')
        )

        with self.assertRaises(ValidationError):
            account.full_clean()
