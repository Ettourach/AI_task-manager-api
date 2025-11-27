from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import TaskViewSet, TagViewSet, ReminderViewSet, DashboardView

# --- DRF Router for endpoints ---
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'reminders', ReminderViewSet, basename='reminder')

# --- URL patterns ---
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
]