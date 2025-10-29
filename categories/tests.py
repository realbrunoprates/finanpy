from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


class CategoryDeletionValidationTests(TestCase):
    """Garante que categorias com transações não sejam excluídas."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='user_category',
            email='user_category@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

        self.account = Account.objects.create(
            user=self.user,
            name='Conta Despesas',
            bank_name='Banco Teste',
            balance=500
        )

    def test_category_with_transactions_cannot_be_deleted(self):
        category = Category.objects.create(
            user=self.user,
            name='Fixas',
            category_type=Category.EXPENSE
        )

        # Transação impede a remoção da categoria utilizada
        Transaction.objects.create(
            account=self.account,
            category=category,
            transaction_type=Transaction.EXPENSE,
            amount=150,
            transaction_date=date.today()
        )

        response = self.client.post(
            reverse('categories:category_delete', args=[category.pk]),
            follow=True
        )

        self.assertTrue(Category.objects.filter(pk=category.pk).exists())

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn(
            (
                'Não é possível excluir esta categoria pois ela possui '
                'transações associadas.'
            ),
            messages,
        )
