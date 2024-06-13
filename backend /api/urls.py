# api/urls.py

from django.urls import path
from .views import get_competitions, get_competitors, get_matches

urlpatterns = [
    path('competitions/', get_competitions, name='get_competitions'),
    path('competitions/<competition_id>/competitors/', get_competitors, name='get_competitors'),
    path('competitions/<competition_id>/matches/', get_matches, name='get_matches'),
]
