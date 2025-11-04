from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse


class AuthenticationViewTests(TestCase):
    """Valida fluxos de signup, login e logout."""

    def setUp(self):
        self.user_model = get_user_model()

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse('users:signup'),
            data={
                'username': 'newuser',
                'email': 'newuser@example.com',
                'password1': 'ComplexPass123!',
                'password2': 'ComplexPass123!',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(
            self.user_model.objects.filter(email='newuser@example.com').exists()
        )
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = [message.message for message in get_messages(
            response.wsgi_request
        )]
        self.assertIn(
            'Conta criada com sucesso! Bem-vindo ao Finanpy.',
            messages,
        )

    def test_login_with_valid_credentials_redirects_to_dashboard(self):
        self.user_model.objects.create_user(
            username='authuser',
            email='authuser@example.com',
            password='ComplexPass123!',
        )

        response = self.client.post(
            reverse('users:login'),
            data={
                'email': 'authuser@example.com',
                'password': 'ComplexPass123!',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('dashboard'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

        messages = [message.message for message in get_messages(
            response.wsgi_request
        )]
        self.assertIn('Bem-vindo de volta!', messages)

    def test_login_with_invalid_credentials_shows_error(self):
        self.user_model.objects.create_user(
            username='invaliduser',
            email='invalid@example.com',
            password='ComplexPass123!',
        )

        response = self.client.post(
            reverse('users:login'),
            data={
                'email': 'invalid@example.com',
                'password': 'WrongPassword!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)
        self.assertIn(
            'E-mail ou senha inválidos.',
            response.context['form'].non_field_errors(),
        )

    def test_logout_clears_session_and_adds_message(self):
        user = self.user_model.objects.create_user(
            username='logoutuser',
            email='logout@example.com',
            password='ComplexPass123!',
        )
        self.client.force_login(user)

        response = self.client.post(
            reverse('users:logout'),
            follow=True,
        )

        self.assertRedirects(response, '/')
        self.assertFalse(response.wsgi_request.user.is_authenticated)

        messages = [message.message for message in get_messages(
            response.wsgi_request
        )]
        self.assertIn('Você saiu com sucesso.', messages)
