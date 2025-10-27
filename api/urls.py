from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, suggest_task

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('suggest_task/', suggest_task, name='suggest_task'),
]