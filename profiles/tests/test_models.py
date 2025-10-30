from django.contrib.auth import get_user_model
from django.test import TestCase

class TestProfileModel(TestCase):
    """Tests for the Profile model behaviour."""

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='profile@example.com',
            password='secure-pass'
        )
        self.profile = self.user.profile

    def test_profile_str_uses_full_name_when_available(self):
        """__str__ should prioritise the full name when provided."""
        self.profile.full_name = 'John Doe'
        self.profile.phone = '11999999999'
        self.profile.save()

        self.assertEqual(str(self.profile), 'John Doe')

    def test_profile_str_falls_back_to_email(self):
        """__str__ should fallback to the associated user email."""
        self.profile.full_name = ''
        self.profile.phone = ''
        self.profile.save()

        self.assertEqual(str(self.profile), 'profile@example.com')
