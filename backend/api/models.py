# api/models.py

from django.db import models

class Team(models.Model):
    team_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=50)
    logo_url = models.URLField(blank=True, null=True)
    players = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Match(models.Model):
    match_id = models.CharField(max_length=100, unique=True)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    league = models.CharField(max_length=100)
    score = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20)
    events = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team}"
