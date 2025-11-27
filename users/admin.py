from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'timezone', 'theme', 'language')
    list_filter = ('theme', 'language')
    search_fields = ('user__username', 'user__email')
