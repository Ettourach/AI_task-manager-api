from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from dotenv import load_dotenv
import openai
import os

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# --------------------------
# User Authentication Views
# --------------------------

def signup(request):
    """Handle user signup with Django’s built-in form."""
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
# Task CRUD API
# --------------------------

class TaskViewSet(viewsets.ModelViewSet):
    """CRUD operations for Task model."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # optional: allow anonymous tasks


# --------------------------
# AI Task Suggestion API
# --------------------------

@api_view(["POST"])
def suggest_task(request):
    """
    AI endpoint: Suggest a task idea based on a given prompt.
    Example POST body: {"prompt": "study Python"}
    """
    try:
        prompt = request.data.get("prompt", "")
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Suggest a task idea related to: {prompt}",
            max_tokens=30,
        )

        suggestion = response.choices[0].text.strip()
        return Response({"suggestion": suggestion})

    except Exception as e:
        return Response({"error": str(e)}, status=400)
