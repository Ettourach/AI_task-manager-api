"""Views for the API app."""

import logging
import os

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from dotenv import load_dotenv
import openai
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Task
from .serializers import TaskSerializer

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Configure OpenAI (old SDK style for v0.28.0)
openai.api_key = os.getenv("OPENAI_API_KEY")


# --------------------------
# User Authentication Views
# --------------------------


def signup(request):
    """Handle user signup using Django's form."""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
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
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def logout_view(request):
    """Logout user."""
    logout(request)
    return redirect("login")


# --------------------------
# Frontend Page
# --------------------------


def index(request):
    """Render main page."""
    return render(request, "index.html")


# --------------------------
# Task CRUD API
# --------------------------


class TaskViewSet(viewsets.ModelViewSet):
    """CRUD operations for Task model (user-specific)."""

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Return tasks belonging only to the authenticated user."""
        if self.request.user.is_authenticated:
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# --------------------------
# AI Task Suggestion API
# --------------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_task(request):
    """
    AI endpoint that suggests a task idea based on user input.
    """
    try:
        prompt = request.data.get("prompt", "").strip()

        if not prompt:
            return Response(
                {"error": "Prompt cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not openai.api_key:
            logger.error("OpenAI API key missing.")
            return Response(
                {"error": "AI service not configured. Contact admin."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # *** Correct API for openai==0.28.0 ***
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that suggests actionable tasks.",
                },
                {
                    "role": "user",
                    "content": f"Suggest a specific task based on: {prompt}",
                },
            ],
            max_tokens=50,
            temperature=0.7,
        )

        suggestion = response["choices"][0]["message"]["content"].strip()

        return Response({"suggestion": suggestion}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in suggest_task: {str(e)}")
        return Response(
            {"error": "Failed to generate task suggestion. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
