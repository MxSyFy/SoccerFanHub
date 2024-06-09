# api/serializers.py

from rest_framework import serializers
from .models import Team, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'country_code', 'type', 'logo_url', 'players']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'home_team', 'away_team', 'start_time', 'end_time', 'location', 'league', 'score', 'status', 'events']
