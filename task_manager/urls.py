from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import TaskViewSet, suggest_task  # make sure 'api' matches your app folder name
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to AI Task Manager API")
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/tasks/suggest/', suggest_task, name='suggest-task'),
]

