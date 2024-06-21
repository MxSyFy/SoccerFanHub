# api/urls.py

from django.urls import path
from .views import CompetitionList, CompetitorList, MatchList, CompetitorMatchList

urlpatterns = [
    path('competitions/', CompetitionList.as_view(), name='get_competitions'),
    path('competitions/<competition_id>/competitors/', CompetitorList.as_view(), name='get_competitors'),
    path('competitions/<competition_id>/matches/', MatchList.as_view(), name='get_matches'),
    path('competitions/<competition_id>/competitors/<competitor_id>/matches/', CompetitorMatchList.as_view(), name='get_competitor_matches'),
]
