from django.urls import path
from .views import toggle_bot

urlpatterns = [
    path('toggle-bot/', toggle_bot, name='toggle-bot'),
]
