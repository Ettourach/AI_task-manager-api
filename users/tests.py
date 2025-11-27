from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse

from .models import Profile


class ProfileModelTestCase(TestCase):
    """Tests for Profile model."""

    def test_profile_auto_created_on_user_creation(self):
        """Test that profile is automatically created when user is created."""
        user = User.objects.create_user(username='testuser', password='testpass')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertEqual(user.profile.user, user)

    def test_profile_default_values(self):
        """Test profile default values."""
        user = User.objects.create_user(username='testuser', password='testpass')
        profile = user.profile
        self.assertEqual(profile.timezone, 'UTC')
        self.assertEqual(profile.theme, 'system')
        self.assertEqual(profile.language, 'en')
        self.assertEqual(profile.notification_preferences, {})


class ProfileAPITestCase(APITestCase):
    """Tests for Profile API endpoint."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_profile(self):
        """Test getting user profile."""
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')
        self.assertEqual(response.data['timezone'], 'UTC')
        self.assertEqual(response.data['theme'], 'system')
        self.assertEqual(response.data['language'], 'en')

    def test_update_profile(self):
        """Test updating user profile."""
        url = reverse('profile')
        data = {
            'timezone': 'America/New_York',
            'theme': 'dark',
            'language': 'es'
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timezone'], 'America/New_York')
        self.assertEqual(response.data['theme'], 'dark')
        self.assertEqual(response.data['language'], 'es')

    def test_update_profile_notification_preferences(self):
        """Test updating notification preferences."""
        url = reverse('profile')
        data = {
            'notification_preferences': {
                'email': True,
                'push': False,
                'reminder_time': 30
            }
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notification_preferences']['email'], True)
        self.assertEqual(response.data['notification_preferences']['push'], False)

    def test_profile_requires_authentication(self):
        """Test that profile endpoint requires authentication."""
        self.client.force_authenticate(user=None)
        url = reverse('profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
