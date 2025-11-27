# models.py
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Tag(models.Model):
    """Tag model for categorizing tasks."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    """Task model with tags, due_date, and completion tracking."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    tags = models.ManyToManyField(Tag, blank=True, related_name='tasks')
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        """Check if the task is overdue."""
        if self.completed:
            return False
        if self.due_date is None:
            return False
        return timezone.now() > self.due_date

    def save(self, *args, **kwargs):
        # If completed status changed to True, set completed_at
        if self.pk:
            old_task = Task.objects.filter(pk=self.pk).only('completed').first()
            if old_task and not old_task.completed and self.completed:
                self.completed_at = timezone.now()
            elif old_task and old_task.completed and not self.completed:
                self.completed_at = None
        elif self.completed and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Reminder(models.Model):
    """Reminder model for task reminders."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='reminders')
    remind_at = models.DateTimeField()
    sent = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['remind_at']

    def __str__(self):
        return f"Reminder for {self.task.title} at {self.remind_at}"