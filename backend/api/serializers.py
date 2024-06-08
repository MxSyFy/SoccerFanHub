# api/serializers.py

from rest_framework import serializers
from .models import Team, Match

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'teamName', 'country', 'league', 'logoURL', 'players']

class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ['id', 'homeTeamId', 'awayTeamId', 'startTime', 'endTime', 'location', 'league', 'score', 'status', 'events']


