from django.contrib.auth import get_user_model
from django.test import TestCase


class TestCustomUserModel(TestCase):
    """Test suite for the CustomUser model and its manager."""

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user_with_email(self):
        """Ensure the custom manager creates users with normalized email."""
        user = self.user_model.objects.create_user(
            email='user@EXAMPLE.COM',
            password='strong-pass-123'
        )

        self.assertEqual(user.email, 'user@example.com')
        self.assertEqual(user.username, 'user@example.com')
        self.assertTrue(user.check_password('strong-pass-123'))

    def test_create_user_without_email_raises_value_error(self):
        """Creating a user without e-mail must raise ValueError."""
        with self.assertRaisesMessage(ValueError, 'O email é obrigatório'):
            self.user_model.objects.create_user(email='', password='pass')

    def test_create_superuser_sets_required_flags(self):
        """Ensure the superuser gets all required permission flags."""
        admin_user = self.user_model.objects.create_superuser(
            email='admin@example.com',
            password='admin-pass'
        )

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_active)

    def test_create_superuser_with_invalid_flags_raises_error(self):
        """Invalid permission flags must raise ValueError for superusers."""
        with self.assertRaisesMessage(
            ValueError,
            'Superusuário precisa ter is_staff=True.'
        ):
            self.user_model.objects.create_superuser(
                email='admin2@example.com',
                password='admin-pass',
                is_staff=False
            )

        with self.assertRaisesMessage(
            ValueError,
            'Superusuário precisa ter is_superuser=True.'
        ):
            self.user_model.objects.create_superuser(
                email='admin3@example.com',
                password='admin-pass',
                is_superuser=False
            )

    def test_str_returns_email(self):
        """__str__ must return the user email."""
        user = self.user_model.objects.create_user(
            email='john.doe@example.com',
            password='test-pass'
        )

        self.assertEqual(str(user), 'john.doe@example.com')
