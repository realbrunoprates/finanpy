from datetime import date

from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from accounts.models import Account
from categories.forms import CategoryForm
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


class CategoryColorValidationTests(TestCase):
    """Valida o formato hexadecimal do campo color."""

    def test_invalid_color_is_rejected(self):
        form = CategoryForm(
            data={
                'name': 'Emergência',
                'category_type': Category.EXPENSE,
                'color': '#gg1234',
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn('Selecione uma cor válida.', form.errors['color'])

    def test_valid_color_is_normalized(self):
        form = CategoryForm(
            data={
                'name': 'Investimentos',
                'category_type': Category.INCOME,
                'color': '#AABBCC',
            }
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['color'], '#aabbcc')


class CategoryCrudViewTests(TestCase):
    """Testa criação, edição, listagem e exclusão de categorias."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='category_owner',
            email='category_owner@example.com',
            password='strong-pass-123'
        )
        self.client.force_login(self.user)

    def test_create_category_assigns_user_and_sets_message(self):
        response = self.client.post(
            reverse('categories:category_create'),
            data={
                'name': 'Viagens',
                'category_type': Category.EXPENSE,
                'color': '#123abc',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('categories:category_list'))

        category = Category.objects.get(name='Viagens')
        self.assertEqual(category.user, self.user)
        self.assertEqual(category.category_type, Category.EXPENSE)
        self.assertEqual(category.color, '#123abc')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Categoria criada com sucesso!', messages)

    def test_update_category_changes_data_for_owner(self):
        category = Category.objects.create(
            user=self.user,
            name='Alimentação Caseira',
            category_type=Category.EXPENSE,
            color='#111111',
        )

        response = self.client.post(
            reverse('categories:category_update', args=[category.pk]),
            data={
                'name': 'Alimentação Fora',
                'category_type': Category.EXPENSE,
                'color': '#222222',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('categories:category_list'))

        category.refresh_from_db()
        self.assertEqual(category.name, 'Alimentação Fora')
        self.assertEqual(category.color, '#222222')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Categoria atualizada com sucesso!', messages)

    def test_list_view_filters_by_search_term(self):
        Category.objects.create(
            user=self.user,
            name='Academia Adicional',
            category_type=Category.INCOME,
            color='#00ff00',
        )
        Category.objects.create(
            user=self.user,
            name='Academia Mensal',
            category_type=Category.EXPENSE,
            color='#ff0000',
        )
        other_user = get_user_model().objects.create_user(
            username='intruder',
            email='intruder@example.com',
            password='strong-pass-123',
        )
        Category.objects.create(
            user=other_user,
            name='Academia Terceiro',
            category_type=Category.INCOME,
            color='#abcdef',
        )

        response = self.client.get(
            reverse('categories:category_list'),
            {'search': 'Academia'},
        )

        self.assertEqual(response.status_code, 200)
        income_names = {
            category.name for category in response.context['income_categories']
        }
        expense_names = {
            category.name for category in response.context['expense_categories']
        }

        self.assertIn('Academia Adicional', income_names)
        self.assertNotIn('Academia Terceiro', income_names)
        self.assertIn('Academia Mensal', expense_names)

    def test_delete_category_without_transactions(self):
        category = Category.objects.create(
            user=self.user,
            name='Cursos',
            category_type=Category.EXPENSE,
            color='#aa00aa',
        )

        response = self.client.post(
            reverse('categories:category_delete', args=[category.pk]),
            follow=True,
        )

        self.assertRedirects(response, reverse('categories:category_list'))
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Categoria excluída com sucesso!', messages)

    def test_user_cannot_edit_category_of_another_user(self):
        other_user = get_user_model().objects.create_user(
            username='category_intruder',
            email='category_intruder@example.com',
            password='strong-pass-123',
        )
        foreign_category = Category.objects.create(
            user=other_user,
            name='Categoria Alheia',
            category_type=Category.EXPENSE,
            color='#333333',
        )

        response = self.client.get(
            reverse('categories:category_update', args=[foreign_category.pk]),
        )

        self.assertEqual(response.status_code, 404)
