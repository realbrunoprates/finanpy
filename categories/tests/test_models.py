from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from categories.models import Category


class TestCategoryModel(TestCase):
    """Tests for the Category model."""

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='category@example.com',
            password='safe-pass'
        )
        self.default_category = self.user.categories.get(name='Alimentação')

    def test_category_str_returns_name(self):
        """__str__ must return the category name."""
        self.assertEqual(str(self.default_category), 'Alimentação')

    def test_unique_category_name_per_user(self):
        """The same user cannot reuse category names."""
        duplicate = Category(
            user=self.user,
            name='Alimentação',
            category_type=Category.EXPENSE
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()

    def test_default_color_is_applied(self):
        """Ensure the default color is used when none is provided."""
        category = Category.objects.create(
            user=self.user,
            name='Viagem',
            category_type=Category.INCOME
        )

        self.assertEqual(category.color, '#667eea')
