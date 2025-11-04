from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class AccountDeletionValidationTests(TestCase):
    """Valida que contas com transações não podem ser removidas."""

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

        # Cria despesa vinculada para simular conta em uso
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

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn(
            (
                'Não é possível excluir esta conta pois ela possui '
                'transações associadas.'
            ),
            messages,
        )


class AccountListPaginationTests(TestCase):
    """Verifica paginação e opções de itens exibidos em contas."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='account_pagination',
            email='account_pagination@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

        # Popula doze contas para testar diferentes tamanhos de página
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


class AccountCrudViewTests(TestCase):
    """Cobertura para criação, edição e exclusão de contas."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='crud_user',
            email='crud_user@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

    def test_create_view_assigns_owner_and_sets_success_message(self):
        response = self.client.post(
            reverse('accounts:create'),
            data={
                'name': 'Conta Poupança',
                'bank_name': 'Banco Seguro',
                'balance': '2500.50',
                'account_type': Account.SAVINGS,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:list'))

        account = Account.objects.get(name='Conta Poupança')
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.bank_name, 'Banco Seguro')
        self.assertEqual(str(account.balance), '2500.50')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Conta criada com sucesso!', messages)

    def test_update_view_persists_changes_for_owner(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Corrente',
            bank_name='Banco Original',
            balance=1000,
        )

        response = self.client.post(
            reverse('accounts:update', args=[account.pk]),
            data={
                'name': 'Conta Corrente Editada',
                'bank_name': 'Banco Atualizado',
                'balance': '1500.00',
                'account_type': Account.CHECKING,
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:list'))

        account.refresh_from_db()
        self.assertEqual(account.name, 'Conta Corrente Editada')
        self.assertEqual(account.bank_name, 'Banco Atualizado')
        self.assertEqual(str(account.balance), '1500.00')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Conta atualizada com sucesso!', messages)

    def test_delete_view_removes_account_without_transactions(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Sem Uso',
            bank_name='Banco Limpo',
            balance=300,
        )

        response = self.client.post(
            reverse('accounts:delete', args=[account.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('accounts:list'))
        self.assertFalse(Account.objects.filter(pk=account.pk).exists())

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Conta excluída com sucesso!', messages)

    def test_user_cannot_access_account_of_another_user(self):
        other_user = get_user_model().objects.create_user(
            username='intruder_account',
            email='intruder_account@example.com',
            password='strong-pass-123',
        )
        foreign_account = Account.objects.create(
            user=other_user,
            name='Conta Estrangeira',
            bank_name='Banco Remoto',
            balance=100,
        )

        response = self.client.get(
            reverse('accounts:update', args=[foreign_account.pk]),
        )

        self.assertEqual(response.status_code, 404)
