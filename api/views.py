from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
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


# basic HTML frontend with a simple form to add/view tasks via API
def index(request):
    return render(request, 'index.html')

#  Task ViewSet — handles CRUD operations for Task model
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # Allow anonymous task creation (optional)


# AI Task Suggestion Endpoint
@api_view(['POST'])
def suggest_task(request):
    """
        AI endpoint: Suggest a task idea based on a given prompt.
        Example POST body: {"prompt": "study Python"}
        """
    try:
        prompt = request.data.get('prompt', '')
        openai.api_key = os.getenv('OPENAI_API_KEY')

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Suggest a task idea related to: {prompt}",
            max_tokens=30
        )

        suggestion = response.choices[0].text.strip()
        return Response({"suggestion": suggestion})

    except Exception as e:
        return Response({"error": str(e)}, status=400)