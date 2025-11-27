from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task, Tag, Reminder
from .serializers import TaskSerializer, TagSerializer, ReminderSerializer


# --------------------------
# User Authentication Views
# --------------------------

def signup(request):
    """Handle user signup with Django's built-in form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # redirect to login page
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    """Custom login view."""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")  # redirect to home page
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Logout user and redirect to login page."""
    logout(request)
    return redirect("login")


# --------------------------
# Frontend Home Page
# --------------------------

def index(request):
    """Basic frontend page."""
    return render(request, "index.html")


# --------------------------
# Tag CRUD API
# --------------------------

class TagViewSet(viewsets.ModelViewSet):
    """CRUD operations for Tag model."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'slug'


# --------------------------
# Task CRUD API
# --------------------------

class TaskViewSet(viewsets.ModelViewSet):
    """CRUD operations for Task model with filtering by tags."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'tags__slug': ['exact', 'in'],
        'completed': ['exact'],
        'due_date': ['gte', 'lte', 'exact'],
    }

    def get_queryset(self):
        """Filter tasks by owner."""
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        """Set owner and user on creation."""
        serializer.save(user=self.request.user, owner=self.request.user)


# --------------------------
# Reminder CRUD API
# --------------------------

class ReminderViewSet(viewsets.ModelViewSet):
    """CRUD operations for Reminder model."""
    queryset = Reminder.objects.all()
    serializer_class = ReminderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter reminders by creator."""
        return Reminder.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        """Set created_by on creation."""
        serializer.save(created_by=self.request.user)


# --------------------------
# Dashboard KPIs API
# --------------------------

class DashboardView(APIView):
    """Dashboard endpoint with KPIs."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Return dashboard KPIs."""
        user = request.user

        # Get completed count
        completed_count = Task.objects.filter(
            owner=user, 
            completed=True
        ).count()

        # Get tasks per category (using tags)
        tasks_per_category = list(
            Task.objects.filter(owner=user)
            .values('tags__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Calculate average completion time in seconds
        completed_tasks = Task.objects.filter(
            owner=user,
            completed=True,
            completed_at__isnull=False
        )
        
        avg_completion_time = None
        if completed_tasks.exists():
            # Calculate average time from created_at to completed_at
            completion_times = []
            for task in completed_tasks:
                delta = task.completed_at - task.created_at
                completion_times.append(delta.total_seconds())
            if completion_times:
                avg_completion_time = sum(completion_times) / len(completion_times)

        # Calculate productivity score (completed tasks / total tasks * 100)
        total_tasks = Task.objects.filter(owner=user).count()
        productivity_score = 0
        if total_tasks > 0:
            productivity_score = round((completed_count / total_tasks) * 100, 2)

        return Response({
            'completed_count': completed_count,
            'tasks_per_category': tasks_per_category,
            'avg_completion_time': avg_completion_time,
            'productivity_score': productivity_score,
        })
