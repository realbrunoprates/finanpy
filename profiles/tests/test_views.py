from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from profiles.models import Profile


class ProfileViewTests(TestCase):
    """Valida exibição e atualização do perfil do usuário."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='profile_user',
            email='profile_user@example.com',
            password='strong-pass-123',
        )
        self.profile = Profile.objects.get(user=self.user)
        self.client.force_login(self.user)

    def test_detail_view_returns_logged_user_profile(self):
        response = self.client.get(reverse('profiles:profile_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['profile'], self.profile)
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')

        breadcrumbs = response.context['breadcrumbs']
        self.assertEqual(
            breadcrumbs,
            [
                {'label': 'Home', 'url': 'home'},
                {'label': 'Perfil', 'url': None},
            ],
        )

    def test_update_view_updates_profile_and_adds_message(self):
        response = self.client.post(
            reverse('profiles:profile_update'),
            data={
                'full_name': 'Usuário Completo',
                'phone': '+55 11 99999-9999',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('profiles:profile_detail'))

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.full_name, 'Usuário Completo')
        self.assertEqual(self.profile.phone, '+55 11 99999-9999')

        messages = [
            message.message
            for message in get_messages(response.wsgi_request)
        ]
        self.assertIn('Perfil atualizado com sucesso!', messages)
