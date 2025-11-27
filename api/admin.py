from django.contrib import admin
from .models import Task, Tag, Reminder


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'completed', 'due_date', 'completed_at', 'created_at')
    list_filter = ('completed', 'created_at', 'due_date', 'tags')
    search_fields = ('title', 'description', 'user__username')
    filter_horizontal = ('tags',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'remind_at', 'sent', 'created_by', 'created_at')
    list_filter = ('sent', 'remind_at', 'created_at')
    search_fields = ('task__title', 'created_by__username')
