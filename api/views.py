from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import viewsets, permissions
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# --------------------------
# Frontend Views
# --------------------------

def home_view(request):
    """Landing page / home"""
    return render(request, 'index.html')


def index(request):
    """Frontend page for tasks (same as home)"""
    return render(request, "index.html")


# --------------------------
# Authentication Views
# --------------------------

def signup_view(request):
    """User signup view"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def login_view(request):
    """User login view"""
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """User logout view (must be POST request)"""
    if request.method == "POST":
        logout(request)
        return redirect("login")

# --------------------------
# Task CRUD API
# --------------------------

class TaskViewSet(viewsets.ModelViewSet):
    """CRUD operations for Task model"""
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only the tasks of the authenticated user
        user = self.request.user
        if user.is_authenticated:
            return Task.objects.filter(user=user)
        return Task.objects.none()  # 👈 if not authenticated, return empty list

    def perform_create(self, serializer):
        # Attach the logged-in user to the task automatically
        serializer.save(user=self.request.user)


# --------------------------
# AI Task Suggestion API
# --------------------------

@api_view(["POST"])
def suggest_task(request):
    """
    AI endpoint: Suggest a task idea based on a given prompt.
    POST body example: {"prompt": "study Python"}
    """
    try:
        prompt = request.data.get("prompt", "")
        if not prompt:
            return Response({"error": "Prompt is required"}, status=400)

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Suggest a task idea related to: {prompt}",
            max_tokens=30,
        )

        suggestion = response.choices[0].text.strip()
        return Response({"suggestion": suggestion})

    except Exception as e:
        return Response({"error": str(e)}, status=400)
