from django.db import models
from django.contrib.auth.models import User


class AISuggestionLog(models.Model):
    """Log model for AI suggestion requests."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_suggestion_logs')
    prompt = models.TextField()
    suggestion = models.TextField()
    used_openai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Suggestion for {self.user.username} at {self.created_at}"
