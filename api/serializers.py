"""Serializers for the API app."""

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with owner information."""

    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "completed",
            "created_at",
            "owner",
            "owner_username",
        ]
        read_only_fields = ["id", "created_at", "owner", "owner_username"]

    def validate_title(self, value):
        """Validate that title is not empty or only whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value.strip()
