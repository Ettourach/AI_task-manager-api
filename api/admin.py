"""Admin configuration for the API app."""

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Admin interface for Task model."""

    list_display = ("id", "title", "owner", "completed", "created_at")
    list_filter = ("completed", "created_at", "owner")
    search_fields = ("title", "description", "owner__username")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
