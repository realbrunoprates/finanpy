from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class TransactionViewTests(TestCase):
    """Testa listagem, criação, edição e exclusão de transações."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='transaction_user',
            email='transaction_user@example.com',
            password='strong-pass-123',
        )
        self.client.force_login(self.user)

        self.income_category = Category.objects.filter(
            user=self.user,
            category_type=Category.INCOME,
        ).first()
        if self.income_category is None:
            self.income_category = Category.objects.create(
                user=self.user,
                name='Receita Extra',
                category_type=Category.INCOME,
                color='#00ff00',
            )
        self.expense_category = Category.objects.filter(
            user=self.user,
            category_type=Category.EXPENSE,
        ).first()
        if self.expense_category is None:
            self.expense_category = Category.objects.create(
                user=self.user,
                name='Despesa Extra',
                category_type=Category.EXPENSE,
                color='#ff0000',
            )
        self.account = Account.objects.create(
            user=self.user,
            name='Conta Principal',
            bank_name='Banco Central',
            balance=1000,
        )

    def test_list_view_returns_only_user_transactions_with_statistics(self):
        income_transaction = Transaction.objects.create(
            account=self.account,
            category=self.income_category,
            transaction_type=Transaction.INCOME,
            amount=500,
            transaction_date=date.today(),
            description='Pagamento mensal',
        )
        expense_transaction = Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=200,
            transaction_date=date.today(),
            description='Aluguel mensal',
        )
        other_user = get_user_model().objects.create_user(
            username='other_user',
            email='other_user@example.com',
            password='strong-pass-123',
        )
        other_account = Account.objects.create(
            user=other_user,
            name='Conta Secundária',
            bank_name='Banco Alternativo',
            balance=300,
        )
        Transaction.objects.create(
            account=other_account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=50,
            transaction_date=date.today(),
            description='Despesa alheia',
        )

        response = self.client.get(reverse('transactions:list'))

        self.assertEqual(response.status_code, 200)
        transactions_ids = {
            transaction.pk for transaction in response.context['transactions']
        }
        self.assertSetEqual(
            transactions_ids,
            {income_transaction.pk, expense_transaction.pk},
        )
        self.assertEqual(response.context['total_income'], 500)
        self.assertEqual(response.context['total_expense'], 200)
        self.assertEqual(response.context['balance'], 300)

    def test_list_view_supports_search_and_date_filters(self):
        today = date.today()
        Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=80,
            transaction_date=today,
            description='Supermercado semanal',
        )
        Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=60,
            transaction_date=today - timedelta(days=10),
            description='Gasolina',
        )

        response = self.client.get(
            reverse('transactions:list'),
            {
                'search': 'Supermercado',
                'data_inicio': today.strftime('%Y-%m-%d'),
                'data_fim': today.strftime('%Y-%m-%d'),
            },
        )

        self.assertEqual(response.status_code, 200)
        descriptions = [
            transaction.description
            for transaction in response.context['transactions']
        ]
        self.assertEqual(descriptions, ['Supermercado semanal'])

    def test_create_view_creates_transaction_and_adds_message(self):
        response = self.client.post(
            reverse('transactions:create'),
            data={
                'account': self.account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '150.00',
                'transaction_date': date.today().strftime('%Y-%m-%d'),
                'description': 'Conta de luz',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('transactions:list'))
        transaction = Transaction.objects.get(description='Conta de luz')
        self.assertEqual(transaction.account, self.account)
        self.assertEqual(transaction.category, self.expense_category)

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn(
            (
                'Transação de despesa criada com sucesso! '
                'O saldo da conta foi atualizado automaticamente.'
            ),
            messages,
        )

    def test_update_view_updates_transaction_fields(self):
        transaction = Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=90,
            transaction_date=date.today(),
            description='Assinatura mensal',
        )

        response = self.client.post(
            reverse('transactions:update', args=[transaction.pk]),
            data={
                'account': self.account.pk,
                'category': self.expense_category.pk,
                'transaction_type': Transaction.EXPENSE,
                'amount': '120.00',
                'transaction_date': date.today().strftime('%Y-%m-%d'),
                'description': 'Assinatura anual',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('transactions:list'))

        transaction.refresh_from_db()
        self.assertEqual(str(transaction.amount), '120.00')
        self.assertEqual(transaction.description, 'Assinatura anual')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Transação atualizada com sucesso!', messages)

    def test_delete_view_removes_transaction_and_sets_message(self):
        transaction = Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=45,
            transaction_date=date.today(),
            description='Taxi eventual',
        )

        response = self.client.post(
            reverse('transactions:delete', args=[transaction.pk]),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('transactions:list'))
        self.assertFalse(Transaction.objects.filter(pk=transaction.pk).exists())

    def test_user_cannot_update_transaction_from_other_user(self):
        other_user = get_user_model().objects.create_user(
            username='transaction_intruder',
            email='transaction_intruder@example.com',
            password='strong-pass-123',
        )
        other_account = Account.objects.create(
            user=other_user,
            name='Conta Alheia',
            bank_name='Banco Distant',
            balance=500,
        )
        other_category = Category.objects.create(
            user=other_user,
            name='Categoria Alheia',
            category_type=Category.EXPENSE,
            color='#aaaaaa',
        )
        foreign_transaction = Transaction.objects.create(
            account=other_account,
            category=other_category,
            transaction_type=Transaction.EXPENSE,
            amount=30,
            transaction_date=date.today(),
            description='Despesa remota',
        )

        response = self.client.get(
            reverse('transactions:update', args=[foreign_transaction.pk]),
        )

        self.assertEqual(response.status_code, 404)
