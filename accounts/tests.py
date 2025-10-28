from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class AccountDeletionValidationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user_account',
            email='user_account@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

        self.expense_category = Category.objects.create(
            user=self.user,
            name='Despesas Gerais',
            category_type=Category.EXPENSE
        )

    def test_account_with_transactions_cannot_be_deleted(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Principal',
            bank_name='Banco Exemplo',
            balance=500
        )

        Transaction.objects.create(
            account=account,
            category=self.expense_category,
            transaction_type=Transaction.EXPENSE,
            amount=100,
            transaction_date=date.today()
        )

        response = self.client.post(
            reverse('accounts:delete', args=[account.pk]),
            follow=True
        )

        self.assertTrue(Account.objects.filter(pk=account.pk).exists())

        messages = [message.message for message in get_messages(response.wsgi_request)]
        self.assertIn(
            'Não é possível excluir esta conta pois ela possui transações associadas.',
            messages
        )


class AccountListPaginationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='account_pagination',
            email='account_pagination@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

        for index in range(12):
            Account.objects.create(
                user=self.user,
                name=f'Conta {index}',
                bank_name='Banco Paginacao',
                balance=100 + index
            )

    def test_account_list_uses_default_paginate_by(self):
        response = self.client.get(reverse('accounts:list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 9)
        self.assertEqual(
            response.context['page_obj'].paginator.count,
            12
        )
        self.assertEqual(response.context['current_per_page'], 9)

    def test_account_list_accepts_valid_per_page_parameter(self):
        response = self.client.get(
            reverse('accounts:list'),
            {'per_page': 6}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 6)
        self.assertEqual(response.context['current_per_page'], 6)
        self.assertEqual(
            response.context['page_obj'].paginator.count,
            12
        )

    def test_account_list_ignores_invalid_per_page_parameter(self):
        response = self.client.get(
            reverse('accounts:list'),
            {'per_page': 99}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['accounts']), 9)
        self.assertEqual(response.context['current_per_page'], 9)
