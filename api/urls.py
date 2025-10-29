from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskViewSet, suggest_task

# --- DRF Router for Task endpoints ---
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# --- URL patterns ---
urlpatterns = [
    path('', include(router.urls)),  # Auto-register CRUD routes from router
    path('suggest-task/', suggest_task, name='suggest-task'),  # AI endpoint
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]