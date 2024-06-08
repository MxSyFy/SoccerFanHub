# hub/urls.py

from django.contrib import admin
from django.urls import path
from api.views import TeamView, MatchView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/teams/', TeamView.as_view(), name='teams'),
    path('api/teams/<int:pk>/', TeamView.as_view(), name='team-detail'),
    path('api/matches/', MatchView.as_view(), name='matches'),
    path('api/matches/<int:pk>/', MatchView.as_view(), name='match-detail'),
]
