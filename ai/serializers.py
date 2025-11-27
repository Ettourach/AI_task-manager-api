from rest_framework import serializers
from .models import AISuggestionLog


class SuggestTaskRequestSerializer(serializers.Serializer):
    """Serializer for AI suggestion request."""
    prompt = serializers.CharField(max_length=500, required=True)


class SuggestTaskResponseSerializer(serializers.Serializer):
    """Serializer for AI suggestion response."""
    suggestion = serializers.CharField()
    used_openai = serializers.BooleanField()


class AISuggestionLogSerializer(serializers.ModelSerializer):
    """Serializer for AISuggestionLog model."""
    class Meta:
        model = AISuggestionLog
        fields = ['id', 'user', 'prompt', 'suggestion', 'used_openai', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
