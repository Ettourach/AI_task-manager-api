from django.shortcuts import render

import os
import openai
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from dotenv import load_dotenv

from .models import AISuggestionLog
from .serializers import SuggestTaskRequestSerializer, SuggestTaskResponseSerializer

# Load environment variables
load_dotenv()


class AISuggestRateThrottle(UserRateThrottle):
    """Rate limiting for AI suggestions: 5/min."""
    scope = 'ai_suggest'
    rate = '5/min'


def get_rule_based_suggestion(prompt):
    """Fallback rule-based suggestion when OpenAI is unavailable."""
    prompt_lower = prompt.lower()
    
    if 'study' in prompt_lower or 'learn' in prompt_lower:
        return "Break down your study session into 25-minute focused blocks using the Pomodoro technique."
    elif 'exercise' in prompt_lower or 'workout' in prompt_lower:
        return "Start with a 10-minute warm-up, then do 30 minutes of cardio or strength training."
    elif 'work' in prompt_lower or 'project' in prompt_lower:
        return "Create a task breakdown with clear milestones and deadlines for your project."
    elif 'read' in prompt_lower or 'book' in prompt_lower:
        return "Set a daily reading goal of 20 pages and track your progress."
    elif 'clean' in prompt_lower or 'organize' in prompt_lower:
        return "Start with one room at a time, declutter first, then organize by category."
    elif 'cook' in prompt_lower or 'meal' in prompt_lower:
        return "Plan your meals for the week and prepare a shopping list based on recipes."
    else:
        return f"Create a detailed action plan for: {prompt}. Break it into smaller, manageable steps."


class SuggestTaskView(APIView):
    """AI endpoint: Suggest a task idea based on a given prompt."""
    permission_classes = [IsAuthenticated]
    throttle_classes = [AISuggestRateThrottle]

    def post(self, request):
        """Handle POST request for AI task suggestion."""
        serializer = SuggestTaskRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        prompt = serializer.validated_data['prompt']
        used_openai = False
        suggestion = None

        # Try OpenAI first
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            try:
                openai.api_key = api_key
                response = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"Suggest a task idea related to: {prompt}",
                    max_tokens=50,
                )
                suggestion = response.choices[0].text.strip()
                used_openai = True
            except Exception:
                # Fallback to rule-based suggestion
                suggestion = get_rule_based_suggestion(prompt)
        else:
            # No API key, use rule-based suggestion
            suggestion = get_rule_based_suggestion(prompt)

        # Log the suggestion
        AISuggestionLog.objects.create(
            user=request.user,
            prompt=prompt,
            suggestion=suggestion,
            used_openai=used_openai
        )

        response_serializer = SuggestTaskResponseSerializer({
            'suggestion': suggestion,
            'used_openai': used_openai
        })
        return Response(response_serializer.data)
