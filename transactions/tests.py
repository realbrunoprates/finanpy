from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import connection
from django.test import TestCase
from django.test.utils import CaptureQueriesContext
from django.urls import reverse
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


class TransactionListViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='transaction_list',
            email='transaction_list@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

        self.account = Account.objects.create(
            user=self.user,
            name='Conta Lista',
            bank_name='Banco Lista',
            balance=Decimal('1000.00')
        )

        self.income_category = Category.objects.create(
            user=self.user,
            name='Receitas Diversas',
            category_type=Category.INCOME
        )

        self.expense_category = Category.objects.create(
            user=self.user,
            name='Despesas Diversas',
            category_type=Category.EXPENSE
        )

        base_date = timezone.localdate()
        self.transactions = []

        for index in range(12):
            transaction_type = (
                Transaction.INCOME
                if index % 2 == 0
                else Transaction.EXPENSE
            )
            category = (
                self.income_category
                if transaction_type == Transaction.INCOME
                else self.expense_category
            )
            amount_value = Decimal(str((index + 1) * 10))

            transaction = Transaction.objects.create(
                account=self.account,
                category=category,
                transaction_type=transaction_type,
                amount=amount_value,
                transaction_date=base_date - timedelta(days=index),
                description=f'Transacao {index}'
            )
            self.transactions.append(transaction)

    def test_transaction_list_default_ordering_is_date_desc(self):
        response = self.client.get(reverse('transactions:list'))

        self.assertEqual(response.status_code, 200)
        page_transactions = list(response.context['page_obj'])

        self.assertEqual(page_transactions[0], self.transactions[0])
        self.assertEqual(response.context['current_sort'], 'date')
        self.assertEqual(response.context['current_direction'], 'desc')

    def test_transaction_list_supports_sorting_by_amount(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'sort': 'amount', 'direction': 'asc'}
        )

        self.assertEqual(response.status_code, 200)
        page_transactions = list(response.context['page_obj'])

        self.assertEqual(page_transactions[0], self.transactions[0])
        self.assertEqual(response.context['current_sort'], 'amount')
        self.assertEqual(response.context['current_direction'], 'asc')

    def test_transaction_list_per_page_override(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'per_page': 10}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['page_obj']), 10)
        self.assertEqual(response.context['current_per_page'], 10)

    def test_transaction_list_invalid_sort_falls_back_to_default(self):
        response = self.client.get(
            reverse('transactions:list'),
            {'sort': 'invalid', 'direction': 'asc'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_sort'], 'date')
        self.assertEqual(response.context['current_direction'], 'desc')

    def test_transaction_list_avoids_n_plus_one_queries(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get(reverse('transactions:list'))

        self.assertEqual(response.status_code, 200)

        # The query count should remain stable even with multiple related objects
        self.assertLessEqual(len(queries.captured_queries), 12)
