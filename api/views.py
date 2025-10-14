from django.http import HttpResponse
from rest_framework import viewsets, status, permissions
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


# Home view — for root URL
def home(request):
    return HttpResponse("Welcome to AI Task Manager API!")


# Task ViewSet
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()  # allow task creation without a user



#  AI Task Suggestion Endpoint
@api_view(['POST'])
def suggest_task(request):
    """
    AI endpoint: Suggest a task description using OpenAI API.
    Example POST body: {"prompt": "Suggest a study task"}
    """
    try:
        prompt = request.data.get('prompt', 'Suggest a productive daily task.')
        response = openai.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=60
        )
        suggestion = response.choices[0].text.strip()
        return Response({'suggestion': suggestion})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)