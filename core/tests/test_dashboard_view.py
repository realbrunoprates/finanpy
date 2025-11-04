from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class DashboardViewTests(TestCase):
    """Garante que o dashboard entregue os resumos financeiros corretos."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='dashboard_user',
            email='dashboard@example.com',
            password='strong-pass-123',
        )
        self.client.force_login(self.user)

        self.account = Account.objects.create(
            user=self.user,
            name='Conta Principal',
            bank_name='Banco Central',
            balance=Decimal('0'),
        )
        self.extra_account = Account.objects.create(
            user=self.user,
            name='Conta Reserva',
            bank_name='Banco Secundário',
            balance=Decimal('200'),
        )
        self.inactive_account = Account.objects.create(
            user=self.user,
            name='Conta Inativa',
            bank_name='Banco Antigo',
            balance=Decimal('50'),
            is_active=False,
        )

        self.income_category = Category.objects.filter(
            user=self.user,
            category_type=Category.INCOME,
        ).first()
        if self.income_category is None:
            self.income_category = Category.objects.create(
                user=self.user,
                name='Receita Primária',
                category_type=Category.INCOME,
                color='#10b981',
            )
        self.expense_category = Category.objects.filter(
            user=self.user,
            category_type=Category.EXPENSE,
        ).first()
        if self.expense_category is None:
            self.expense_category = Category.objects.create(
                user=self.user,
                name='Despesa Principal',
                category_type=Category.EXPENSE,
                color='#ef4444',
            )

        today = timezone.localdate()
        Transaction.objects.create(
            account=self.account,
            category=self.income_category,
            transaction_type=Transaction.INCOME,
            amount=Decimal('1000.00'),
            transaction_date=today,
            description='Salário mensal',
        )
        Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=Decimal('400.00'),
            transaction_date=today,
            description='Aluguel do mês',
        )
        Transaction.objects.create(
            account=self.account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=Decimal('100.00'),
            transaction_date=today - timedelta(days=40),
            description='Despesa antiga',
        )

        self.account.refresh_from_db()
        self.extra_account.refresh_from_db()
        self.inactive_account.refresh_from_db()
        self.total_balance = (
            self.account.balance
            + self.extra_account.balance
            + self.inactive_account.balance
        )

    def test_dashboard_context_includes_financial_summary(self):
        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_balance'], self.total_balance)
        self.assertEqual(
            response.context['total_income_month'],
            Decimal('1000.00'),
        )
        self.assertEqual(
            response.context['total_expenses_month'],
            Decimal('400.00'),
        )
        self.assertEqual(
            response.context['month_balance'],
            Decimal('600.00'),
        )
        self.assertEqual(
            response.context['active_accounts_count'],
            2,
        )

        recent_descriptions = [
            tx.description for tx in response.context['recent_transactions']
        ]
        self.assertIn('Salário mensal', recent_descriptions)
        self.assertIn('Aluguel do mês', recent_descriptions)

        expenses_by_category = list(response.context['expenses_by_category'])
        self.assertEqual(
            expenses_by_category[0]['category__name'],
            self.expense_category.name,
        )
        self.assertEqual(
            expenses_by_category[0]['total'],
            Decimal('400.00'),
        )

        chart_data = response.context['chart_categories_data']
        self.assertEqual(chart_data['labels'], [self.expense_category.name])
        self.assertEqual(chart_data['values'], [400.0])
        self.assertEqual(chart_data['colors'], [self.expense_category.color])


class LoginRequiredViewTests(TestCase):
    """Garante que páginas sensíveis exigem autenticação."""

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/auth/login/'))
        self.assertIn('next=/dashboard/', response.url)

    def test_accounts_list_requires_authentication(self):
        response = self.client.get(reverse('accounts:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('?next=/accounts/', response.url)

    def test_categories_list_requires_authentication(self):
        response = self.client.get(reverse('categories:category_list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('?next=/categories/', response.url)

    def test_transactions_list_requires_authentication(self):
        response = self.client.get(reverse('transactions:list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('?next=/transactions/', response.url)

    def test_profile_detail_requires_authentication(self):
        response = self.client.get(reverse('profiles:profile_detail'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('?next=/profile/', response.url)
