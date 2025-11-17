"""Task model for managing user tasks."""

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    """
    Represents a task with title, description, and completion status.

    Each task is owned by a user and tracks creation time.
    """

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="User who owns this task",
    )
    title = models.CharField(max_length=255, help_text="Title of the task")
    description = models.TextField(
        blank=True, help_text="Detailed description of the task"
    )
    completed = models.BooleanField(
        default=False, help_text="Whether the task is completed"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the task was created"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Task"
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title
