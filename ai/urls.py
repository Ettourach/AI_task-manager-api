from django.urls import path
from .views import SuggestTaskView

urlpatterns = [
    path('suggest-task/', SuggestTaskView.as_view(), name='suggest-task'),
]
