"""Views for the API app."""

import logging
import os

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from openai import OpenAI
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

# Initialize OpenAI client
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


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
    """
    Custom login view.

    GET: Display login form
    POST: Process login form and authenticate user
    """
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
    """
    ViewSet for CRUD operations on Task model.

    Provides list, create, retrieve, update, partial_update, and destroy actions.
    Users can only access their own tasks.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return tasks owned by the current user.

        For unauthenticated users, return empty queryset.
        """
        if self.request.user.is_authenticated:
            return Task.objects.filter(owner=self.request.user)
        return Task.objects.none()

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a task."""
        serializer.save(owner=self.request.user)


# --------------------------
# AI Task Suggestion API
# --------------------------


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def suggest_task(request):
    """
    AI endpoint: Suggest a task idea based on a given prompt.

    Request body: {"prompt": "study Python"}
    Response: {"suggestion": "Create a Python web scraper project"}

    Requires authentication.
    """
    try:
        prompt = request.data.get("prompt", "")

        if not prompt or not prompt.strip():
            return Response(
                {"error": "Prompt cannot be empty."}, status=status.HTTP_400_BAD_REQUEST
            )

        # Check if OpenAI API key is configured
        if not os.getenv("OPENAI_API_KEY"):
            logger.error("OpenAI API key not configured")
            return Response(
                {
                    "error": "AI service is not configured. Please contact administrator."
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        # Use the new ChatCompletion API instead of deprecated Completion API
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that suggests specific, actionable tasks.",
                },
                {
                    "role": "user",
                    "content": f"Suggest a specific task idea related to: {prompt.strip()}",
                },
            ],
            max_tokens=50,
            temperature=0.7,
        )

        suggestion = response.choices[0].message.content.strip()
        return Response({"suggestion": suggestion}, status=status.HTTP_200_OK)

    except Exception as e:
        logger.error(f"Error in suggest_task: {str(e)}")
        return Response(
            {"error": "Failed to generate task suggestion. Please try again later."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
