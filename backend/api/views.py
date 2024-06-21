# api/views.py

from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
import requests

# Sportradar API key and base URL
API_KEY = 'THrKg3qzoKQzdwaFFubG6xUtoIPpAEq5Y6bwiE8g'
BASE_URL = 'https://api.sportradar.com/soccer/trial/v4/en/'

# Cache timeout set to 1 hour (3600 seconds)
CACHE_TIMEOUT = 60 * 60

class CompetitionList(APIView):
    def get(self, request):
        cache_key = 'competitions'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({'competitions': cached_data})
        
        url = f'{BASE_URL}/competitions.json'
        params = {'api_key': API_KEY}
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        filtered_competitions = [
            {
                'id': comp['id'],
                'name': comp['name'],
                'gender': comp['gender'],
                'category': comp['category'],
            }
            for comp in data.get('competitions', [])
            if comp.get('gender') == 'women'
        ]
        
        cache.set(cache_key, filtered_competitions, CACHE_TIMEOUT)
        return Response({'competitions': filtered_competitions})

class CompetitorList(APIView):
    def get(self, request, competition_id):
        cache_key = f'competitors_{competition_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({'competitors': cached_data})
        
        seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
        params = {'api_key': API_KEY}
        
        response = requests.get(seasons_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)
        most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None
        
        if not most_recent_season:
            return Response({'error': 'No seasons found for this competition'}, status=404)
        
        competitors_url = f'{BASE_URL}/seasons/{most_recent_season}/competitors.json'
        response = requests.get(competitors_url, params=params)
        response.raise_for_status()
        
        competitors_data = response.json().get('season_competitors', [])
        competitors = [
            {
                'id': competitor['id'],
                'name': competitor['name'],
                'country': competitor.get('country'),
                'abbreviation': competitor.get('abbreviation'),
                'gender': competitor.get('gender')
            }
            for competitor in competitors_data
        ]
        
        cache.set(cache_key, competitors, CACHE_TIMEOUT)
        return Response({'competitors': competitors})

class MatchList(APIView):
    def get(self, request, competition_id):
        cache_key = f'matches_{competition_id}'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response({'matches': cached_data})
        
        seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
        params = {'api_key': API_KEY}
        
        response = requests.get(seasons_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)
        most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None
        
        if not most_recent_season:
            return Response({'error': 'No seasons found for this competition'}, status=404)
        
        schedules_url = f'{BASE_URL}/seasons/{most_recent_season}/schedules.json'
        response = requests.get(schedules_url, params=params)
        response.raise_for_status()
        
        schedules_data = response.json().get('schedules', [])
        matches = [
            {
                'id': schedule['sport_event']['id'],
                'start_time': schedule['sport_event']['start_time'],
                'home_team': schedule['sport_event']['competitors'][0]['name'],
                'away_team': schedule['sport_event']['competitors'][1]['name'],
                'home_score': schedule['sport_event_status'].get('home_score', 0),
                'away_score': schedule['sport_event_status'].get('away_score', 0),
                'status': schedule['sport_event_status']['status'],
                'winner': schedule['sport_event_status'].get('winner_id', '')
            }
            for schedule in schedules_data
        ]
        
        cache.set(cache_key, matches, CACHE_TIMEOUT)
        return Response({'matches': matches})

class CompetitorMatchList(APIView):
    def get(self, request, competition_id, competitor_id):
        cache_key = f'competitor_matches_{competition_id}_{competitor_id}'
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response({'matches': cached_data})

        seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
        params = {'api_key': API_KEY}

        response = requests.get(seasons_url, params=params)
        response.raise_for_status()
        data = response.json()

        data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)
        most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None

        if not most_recent_season:
            return Response({'error': 'No seasons found for this competition'}, status=404)

        schedules_url = f'{BASE_URL}/seasons/{most_recent_season}/schedules.json'
        response = requests.get(schedules_url, params=params)
        response.raise_for_status()

        schedules_data = response.json().get('schedules', [])
        matches = [
            {
                'id': schedule['sport_event']['id'],
                'start_time': schedule['sport_event']['start_time'],
                'home_team': schedule['sport_event']['competitors'][0]['name'],
                'away_team': schedule['sport_event']['competitors'][1]['name'],
                'home_score': schedule['sport_event_status'].get('home_score', 0),
                'away_score': schedule['sport_event_status'].get('away_score', 0),
                'status': schedule['sport_event_status']['status'],
                'winner': schedule['sport_event_status'].get('winner_id', '')
            }
            for schedule in schedules_data
            if competitor_id in [comp['id'] for comp in schedule['sport_event']['competitors']]
        ]

        cache.set(cache_key, matches, CACHE_TIMEOUT)
        return Response({'matches': matches})

