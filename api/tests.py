from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from io import StringIO
from django.core.management import call_command
from unittest.mock import patch

from .models import Task, Tag, Reminder


class TaskModelTestCase(TestCase):
    """Tests for Task model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_task_creation(self):
        """Test basic task creation."""
        task = Task.objects.create(title="Test Task", owner=self.user)
        self.assertEqual(task.owner.username, "testuser")
        self.assertEqual(task.title, "Test Task")
        self.assertFalse(task.completed)

    def test_task_is_overdue_false_when_no_due_date(self):
        """Test is_overdue is False when no due date set."""
        task = Task.objects.create(title="Test Task", owner=self.user)
        self.assertFalse(task.is_overdue)

    def test_task_is_overdue_false_when_completed(self):
        """Test is_overdue is False when task is completed."""
        task = Task.objects.create(
            title="Test Task",
            owner=self.user,
            due_date=timezone.now() - timedelta(days=1),
            completed=True
        )
        self.assertFalse(task.is_overdue)

    def test_task_is_overdue_true_when_past_due(self):
        """Test is_overdue is True when past due date."""
        task = Task.objects.create(
            title="Test Task",
            owner=self.user,
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(task.is_overdue)

    def test_task_is_overdue_false_when_future_due(self):
        """Test is_overdue is False when future due date."""
        task = Task.objects.create(
            title="Test Task",
            owner=self.user,
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(task.is_overdue)

    def test_completed_at_set_on_completion(self):
        """Test completed_at is set when task is marked completed."""
        task = Task.objects.create(title="Test Task", owner=self.user)
        self.assertIsNone(task.completed_at)
        
        task.completed = True
        task.save()
        task.refresh_from_db()
        
        self.assertIsNotNone(task.completed_at)

    def test_completed_at_cleared_on_uncomplete(self):
        """Test completed_at is cleared when task is marked incomplete."""
        task = Task.objects.create(
            title="Test Task",
            owner=self.user,
            completed=True
        )
        task.refresh_from_db()
        self.assertIsNotNone(task.completed_at)
        
        task.completed = False
        task.save()
        task.refresh_from_db()
        
        self.assertIsNone(task.completed_at)


class TagModelTestCase(TestCase):
    """Tests for Tag model."""

    def test_tag_creation(self):
        """Test tag creation with auto-slug."""
        tag = Tag.objects.create(name="Test Tag")
        self.assertEqual(tag.name, "Test Tag")
        self.assertEqual(tag.slug, "test-tag")

    def test_tag_custom_slug(self):
        """Test tag with custom slug."""
        tag = Tag.objects.create(name="Test Tag", slug="custom-slug")
        self.assertEqual(tag.slug, "custom-slug")


class TagAPITestCase(APITestCase):
    """Tests for Tag API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_tag(self):
        """Test creating a tag."""
        url = reverse('tag-list')
        data = {'name': 'Work'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tag.objects.count(), 1)
        self.assertEqual(Tag.objects.get().name, 'Work')

    def test_list_tags(self):
        """Test listing tags."""
        Tag.objects.create(name='Work')
        Tag.objects.create(name='Personal')
        url = reverse('tag-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_update_tag(self):
        """Test updating a tag."""
        tag = Tag.objects.create(name='Work')
        url = reverse('tag-detail', kwargs={'slug': tag.slug})
        data = {'name': 'Office Work'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, 'Office Work')

    def test_delete_tag(self):
        """Test deleting a tag."""
        tag = Tag.objects.create(name='Work')
        url = reverse('tag-detail', kwargs={'slug': tag.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)


class TaskAPITestCase(APITestCase):
    """Tests for Task API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_create_task_with_tags(self):
        """Test creating a task with tags."""
        tag = Tag.objects.create(name='Work')
        url = reverse('task-list')
        data = {
            'title': 'Test Task',
            'tag_ids': [tag.id]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        task = Task.objects.get()
        self.assertIn(tag, task.tags.all())

    def test_filter_tasks_by_tag_slug(self):
        """Test filtering tasks by tag slug."""
        tag = Tag.objects.create(name='Work')
        task1 = Task.objects.create(title='Work Task', owner=self.user)
        task1.tags.add(tag)
        task2 = Task.objects.create(title='Personal Task', owner=self.user)
        
        url = reverse('task-list') + '?tags__slug=work'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Work Task')


class ReminderModelTestCase(TestCase):
    """Tests for Reminder model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Test Task', owner=self.user)

    def test_reminder_creation(self):
        """Test reminder creation."""
        remind_at = timezone.now() + timedelta(hours=1)
        reminder = Reminder.objects.create(
            task=self.task,
            remind_at=remind_at,
            created_by=self.user
        )
        self.assertEqual(reminder.task, self.task)
        self.assertFalse(reminder.sent)
        self.assertEqual(reminder.created_by, self.user)


class ReminderAPITestCase(APITestCase):
    """Tests for Reminder API endpoints."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.task = Task.objects.create(title='Test Task', owner=self.user)

    def test_create_reminder(self):
        """Test creating a reminder."""
        url = reverse('reminder-list')
        remind_at = timezone.now() + timedelta(hours=1)
        data = {
            'task': self.task.id,
            'remind_at': remind_at.isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reminder.objects.count(), 1)


class SendRemindersCommandTestCase(TestCase):
    """Tests for send_reminders management command."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Test Task', owner=self.user)

    def test_send_reminders_marks_due_as_sent(self):
        """Test that due reminders are marked as sent."""
        reminder = Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() - timedelta(hours=1),
            created_by=self.user
        )
        
        out = StringIO()
        call_command('send_reminders', stdout=out)
        
        reminder.refresh_from_db()
        self.assertTrue(reminder.sent)

    def test_send_reminders_skips_future(self):
        """Test that future reminders are not processed."""
        reminder = Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() + timedelta(hours=1),
            created_by=self.user
        )
        
        out = StringIO()
        call_command('send_reminders', stdout=out)
        
        reminder.refresh_from_db()
        self.assertFalse(reminder.sent)

    def test_send_reminders_dry_run(self):
        """Test dry run doesn't mark reminders as sent."""
        reminder = Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() - timedelta(hours=1),
            created_by=self.user
        )
        
        out = StringIO()
        call_command('send_reminders', '--dry-run', stdout=out)
        
        reminder.refresh_from_db()
        self.assertFalse(reminder.sent)
        self.assertIn('DRY RUN', out.getvalue())


class DashboardAPITestCase(APITestCase):
    """Tests for Dashboard API endpoint."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_dashboard_empty(self):
        """Test dashboard with no tasks."""
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_count'], 0)
        self.assertEqual(response.data['productivity_score'], 0)

    def test_dashboard_with_tasks(self):
        """Test dashboard with tasks."""
        tag = Tag.objects.create(name='Work')
        task1 = Task.objects.create(title='Task 1', owner=self.user, completed=True)
        task1.tags.add(tag)
        task2 = Task.objects.create(title='Task 2', owner=self.user)
        
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['completed_count'], 1)
        self.assertEqual(response.data['productivity_score'], 50.0)

    def test_dashboard_tasks_per_category(self):
        """Test tasks per category in dashboard."""
        tag1 = Tag.objects.create(name='Work')
        tag2 = Tag.objects.create(name='Personal')
        
        task1 = Task.objects.create(title='Work Task 1', owner=self.user)
        task1.tags.add(tag1)
        task2 = Task.objects.create(title='Work Task 2', owner=self.user)
        task2.tags.add(tag1)
        task3 = Task.objects.create(title='Personal Task', owner=self.user)
        task3.tags.add(tag2)
        
        url = reverse('dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tasks_per_category', response.data)


class CeleryTaskTestCase(TestCase):
    """Tests for Celery tasks."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.task = Task.objects.create(title='Test Task', owner=self.user)

    @patch('api.tasks.process_due_reminders.delay')
    def test_process_due_reminders_task(self, mock_delay):
        """Test process_due_reminders celery task can be called."""
        from api.tasks import process_due_reminders
        
        reminder = Reminder.objects.create(
            task=self.task,
            remind_at=timezone.now() - timedelta(hours=1),
            created_by=self.user
        )
        
        # Call the task directly (synchronously for testing)
        result = process_due_reminders()
        
        reminder.refresh_from_db()
        self.assertTrue(reminder.sent)
        self.assertIn('1', result)
