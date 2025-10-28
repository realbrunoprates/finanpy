from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import Account
from categories.models import Category
from transactions.forms import TransactionForm
from transactions.models import Transaction


class TransactionValidationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='transaction_user',
            email='transaction_user@example.com',
            password='strong-pass-123'
        )

        self.expense_category = Category.objects.create(
            user=self.user,
            name='Despesas Variáveis',
            category_type=Category.EXPENSE
        )

    def test_form_rejects_future_transaction_date(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Teste Futuro',
            bank_name='Banco Tempo',
            balance=Decimal('500.00')
        )

        future_date = timezone.localdate() + timedelta(days=1)

        form = TransactionForm(
            data={
                'account': account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '50.00',
                'transaction_date': future_date.isoformat(),
                'description': 'Despesa futura'
            },
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            'A data da transação não pode estar no futuro.',
            form.errors['transaction_date']
        )

    def test_form_rejects_negative_amount(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Valores',
            bank_name='Banco Valores',
            balance=Decimal('500.00')
        )

        form = TransactionForm(
            data={
                'account': account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '-10.00',
                'transaction_date': timezone.localdate().isoformat(),
                'description': 'Despesa inválida'
            },
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            'O valor da transação deve ser maior que zero.',
            form.errors['amount']
        )

    def test_expense_requires_sufficient_balance_on_create(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Saldo',
            bank_name='Banco Saldo',
            balance=Decimal('100.00')
        )

        form = TransactionForm(
            data={
                'account': account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '150.00',
                'transaction_date': timezone.localdate().isoformat(),
                'description': 'Despesa alta'
            },
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Saldo insuficiente na conta selecionada para esta despesa.',
            form.errors['amount']
        )

    def test_expense_update_considers_existing_transaction_balance(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Atualização',
            bank_name='Banco Atualização',
            balance=Decimal('200.00')
        )

        transaction = Transaction.objects.create(
            account=account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=Decimal('50.00'),
            transaction_date=timezone.localdate()
        )

        account.refresh_from_db()

        form = TransactionForm(
            data={
                'account': account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '300.00',
                'transaction_date': timezone.localdate().isoformat(),
                'description': 'Despesa reajustada'
            },
            instance=transaction,
            user=self.user
        )

        self.assertFalse(form.is_valid())
        self.assertIn(
            'Saldo insuficiente na conta selecionada para esta despesa.',
            form.errors['amount']
        )
