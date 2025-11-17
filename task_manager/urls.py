"""URL configuration for the task_manager project."""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.views import index, login_view, logout_view, signup

# API documentation schema
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version="v1",
        description="API documentation for Task Manager backend project",
        contact=openapi.Contact(email="support@taskmanager.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Frontend pages
    path("", index, name="index"),
    # Authentication
    path("accounts/signup/", signup, name="signup"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/", include("django.contrib.auth.urls")),
    # API endpoints
    path("api/", include("api.urls")),
    # API documentation
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
