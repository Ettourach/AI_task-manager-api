from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from unittest.mock import patch, MagicMock

from .models import AISuggestionLog
from .views import get_rule_based_suggestion


class AISuggestionLogModelTestCase(TestCase):
    """Tests for AISuggestionLog model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_suggestion_log_creation(self):
        """Test suggestion log creation."""
        log = AISuggestionLog.objects.create(
            user=self.user,
            prompt='Study Python',
            suggestion='Review Python basics',
            used_openai=True
        )
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.prompt, 'Study Python')
        self.assertTrue(log.used_openai)


class RuleBasedSuggestionTestCase(TestCase):
    """Tests for rule-based suggestions."""

    def test_study_suggestion(self):
        """Test suggestion for study-related prompts."""
        suggestion = get_rule_based_suggestion('study math')
        self.assertIn('Pomodoro', suggestion)

    def test_exercise_suggestion(self):
        """Test suggestion for exercise-related prompts."""
        suggestion = get_rule_based_suggestion('workout plan')
        self.assertIn('warm-up', suggestion)

    def test_work_suggestion(self):
        """Test suggestion for work-related prompts."""
        suggestion = get_rule_based_suggestion('project deadline')
        self.assertIn('task breakdown', suggestion)

    def test_read_suggestion(self):
        """Test suggestion for reading-related prompts."""
        suggestion = get_rule_based_suggestion('read more books')
        self.assertIn('reading goal', suggestion)

    def test_generic_suggestion(self):
        """Test suggestion for generic prompts."""
        suggestion = get_rule_based_suggestion('random task')
        self.assertIn('action plan', suggestion)


class SuggestTaskAPITestCase(APITestCase):
    """Tests for AI Suggest Task API endpoint."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = reverse('suggest-task')

    def test_suggest_task_requires_authentication(self):
        """Test that suggest task requires authentication."""
        self.client.force_authenticate(user=None)
        response = self.client.post(self.url, {'prompt': 'test'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_suggest_task_requires_prompt(self):
        """Test that prompt is required."""
        response = self.client.post(self.url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.dict('os.environ', {'OPENAI_API_KEY': ''})
    def test_suggest_task_fallback_without_api_key(self):
        """Test fallback to rule-based when no API key."""
        response = self.client.post(self.url, {'prompt': 'study Python'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestion', response.data)
        self.assertFalse(response.data['used_openai'])

    @patch('ai.views.openai')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_task_with_openai_success(self, mock_openai):
        """Test successful OpenAI suggestion."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(text='AI generated suggestion')]
        mock_openai.Completion.create.return_value = mock_response
        
        response = self.client.post(self.url, {'prompt': 'test prompt'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch('ai.views.openai')
    @patch.dict('os.environ', {'OPENAI_API_KEY': 'test-key'})
    def test_suggest_task_openai_error_fallback(self, mock_openai):
        """Test fallback to rule-based when OpenAI fails."""
        mock_openai.Completion.create.side_effect = Exception('API Error')
        
        response = self.client.post(self.url, {'prompt': 'study Python'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestion', response.data)
        self.assertFalse(response.data['used_openai'])

    def test_suggestion_logged(self):
        """Test that suggestions are logged."""
        response = self.client.post(self.url, {'prompt': 'test logging'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AISuggestionLog.objects.count(), 1)
        log = AISuggestionLog.objects.first()
        self.assertEqual(log.user, self.user)
        self.assertEqual(log.prompt, 'test logging')
