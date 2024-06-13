# api/models.py

from django.db import models

class Competition(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10)
    category_id = models.CharField(max_length=100)
    category_name = models.CharField(max_length=200)
    country_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Competitor(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=100, blank=True, null=True)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    season_id = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    home_team = models.ForeignKey(Competitor, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Competitor, related_name='away_matches', on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    status = models.CharField(max_length=50)
    winner = models.ForeignKey(Competitor, related_name='won_matches', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.start_time}"
