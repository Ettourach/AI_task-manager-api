"""Tests for the API app."""

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import Task


class TaskModelTestCase(TestCase):
    """Tests for the Task model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.task = Task.objects.create(
            title="Test Task", description="Test description", owner=self.user
        )

    def test_task_creation(self):
        """Test that a task can be created successfully."""
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.owner.username, "testuser")
        self.assertFalse(self.task.completed)

    def test_task_str_representation(self):
        """Test the string representation of a task."""
        self.assertEqual(str(self.task), "Test Task")


class TaskAPITestCase(TestCase):
    """Tests for the Task API endpoints."""

    def setUp(self):
        """Set up test client and user."""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_task(self):
        """Test creating a task via API."""
        data = {
            "title": "New Task",
            "description": "Task description",
            "completed": False,
        }
        response = self.client.post("/api/tasks/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().title, "New Task")

    def test_list_tasks(self):
        """Test listing tasks via API."""
        Task.objects.create(title="Task 1", owner=self.user)
        Task.objects.create(title="Task 2", owner=self.user)

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_update_task(self):
        """Test updating a task via API."""
        task = Task.objects.create(title="Original Title", owner=self.user)
        data = {"title": "Updated Title", "completed": True}

        response = self.client.patch(f"/api/tasks/{task.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        task.refresh_from_db()
        self.assertEqual(task.title, "Updated Title")
        self.assertTrue(task.completed)

    def test_delete_task(self):
        """Test deleting a task via API."""
        task = Task.objects.create(title="Task to delete", owner=self.user)

        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_user_can_only_see_own_tasks(self):
        """Test that users can only see their own tasks."""
        other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        Task.objects.create(title="My Task", owner=self.user)
        Task.objects.create(title="Other Task", owner=other_user)

        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "My Task")
