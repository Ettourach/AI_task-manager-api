from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task

class TaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        Task.objects.create(title="Test Task", owner=self.user)

    def test_task_creation(self):
        task = Task.objects.get(title="Test Task")
        self.assertEqual(task.owner.username, "testuser")