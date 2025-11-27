from rest_framework import serializers
from .models import Task, Tag, Reminder


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model."""
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with tag support."""
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='tags'
    )
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'user', 'title', 'description', 'completed', 
                  'created_at', 'owner', 'tags', 'tag_ids', 'due_date', 
                  'completed_at', 'is_overdue']
        read_only_fields = ['user', 'owner', 'completed_at', 'is_overdue']


class ReminderSerializer(serializers.ModelSerializer):
    """Serializer for Reminder model."""
    class Meta:
        model = Reminder
        fields = ['id', 'task', 'remind_at', 'sent', 'created_by', 'created_at']
        read_only_fields = ['sent', 'created_by', 'created_at']