from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, suggest_task

# Create a router for the TaskViewSet
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),             # /api/tasks/ (list, create)
    path('tasks/suggest/', suggest_task, name='suggest-task'),  # /api/tasks/suggest/
]
