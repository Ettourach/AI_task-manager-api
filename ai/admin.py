from django.contrib import admin
from .models import AISuggestionLog


@admin.register(AISuggestionLog)
class AISuggestionLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'prompt', 'used_openai', 'created_at')
    list_filter = ('used_openai', 'created_at')
    search_fields = ('user__username', 'prompt', 'suggestion')
