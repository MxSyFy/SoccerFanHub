# api/models.py

from django.db import models

class Team(models.Model):
    teamName = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    logoURL = models.URLField()
    players = models.JSONField()
    
    def __str__(self):
        return self.teamName

class Match(models.Model):
    homeTeamId = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    awayTeamId = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    location = models.CharField(max_length=100)
    league = models.CharField(max_length=100)
    score = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20)
    events = models.JSONField(blank=True)
    
    def __str__(self):
        return f"{self.homeTeamId} vs {self.awayTeamId}"
