# api/views.py

from django.core.cache import cache
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

# Sportradar API key and base URL
API_KEY = 'THrKg3qzoKQzdwaFFubG6xUtoIPpAEq5Y6bwiE8g'
BASE_URL = 'https://api.sportradar.com/soccer/trial/v4/en/'

# Cache timeout set to 1 hour (3600 seconds)
CACHE_TIMEOUT = 60 * 60

@api_view(['GET'])
def get_competitions(request):
    cache_key = 'competitions'  # Key to store competitions data in cache
    cached_data = cache.get(cache_key)  # Check if data is already in cache
    
    if cached_data:
        return Response({'competitions': cached_data})  # Return cached data if available
    
    url = f'{BASE_URL}/competitions.json'  # API endpoint for competitions
    params = {'api_key': API_KEY}  # Parameters including API key

    response = requests.get(url, params=params)  # Make the API request
    response.raise_for_status()  # Raise error for bad responses
    data = response.json()  # Parse JSON data from response
    
    filtered_competitions = [
        {
            'id': comp['id'],
            'name': comp['name'],
            'gender': comp['gender'],
            'category': comp['category'],
        }
        for comp in data.get('competitions', [])
        if comp.get('gender') == 'women'  # Filter only women competitions
    ]
    
    cache.set(cache_key, filtered_competitions, CACHE_TIMEOUT)  # Store filtered data in cache
    return Response({'competitions': filtered_competitions})  # Return the data

@api_view(['GET'])
def get_competitors(request, competition_id):
    cache_key = f'competitors_{competition_id}'  # Key to store competitors data in cache
    cached_data = cache.get(cache_key)  # Check if data is already in cache
    
    if cached_data:
        return Response({'competitors': cached_data})  # Return cached data if available
    
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'  # API endpoint for seasons
    params = {'api_key': API_KEY}  # Parameters including API key
    
    response = requests.get(seasons_url, params=params)  # Make the API request
    response.raise_for_status()  # Raise error for bad responses
    data = response.json()  # Parse JSON data from response
    
    # Sort seasons by start date in descending order and get the most recent season
    data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)
    most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None
    
    if not most_recent_season:
        return Response({'error': 'No seasons found for this competition'}, status=404)  # Return error if no seasons found
    
    competitors_url = f'{BASE_URL}/seasons/{most_recent_season}/competitors.json'  # API endpoint for competitors
    response = requests.get(competitors_url, params=params)  # Make the API request
    response.raise_for_status()  # Raise error for bad responses
    
    competitors_data = response.json().get('season_competitors', [])  # Parse JSON data from response
    competitors = [
        {
            'id': competitor['id'],
            'name': competitor['name'],
            'country': competitor.get('country'),
            'abbreviation': competitor.get('abbreviation'),
            'gender': competitor.get('gender')
        }
        for competitor in competitors_data  # Extract relevant fields from competitors data
    ]
    
    cache.set(cache_key, competitors, CACHE_TIMEOUT)  # Store filtered data in cache
    return Response({'competitors': competitors})  # Return the data

@api_view(['GET'])
def get_matches(request, competition_id):
    cache_key = f'matches_{competition_id}'  # Key to store matches data in cache
    cached_data = cache.get(cache_key)  # Check if data is already in cache
    
    if cached_data:
        return Response({'matches': cached_data})  # Return cached data if available
    
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'  # API endpoint for seasons
    params = {'api_key': API_KEY}  # Parameters including API key
    
    response = requests.get(seasons_url, params=params)  # Make the API request
    response.raise_for_status()  # Raise error for bad responses
    data = response.json()  # Parse JSON data from response
    
    # Sort seasons by start date in descending order and get the most recent season
    data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)
    most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None
    
    if not most_recent_season:
        return Response({'error': 'No seasons found for this competition'}, status=404)  # Return error if no seasons found
    
    schedules_url = f'{BASE_URL}/seasons/{most_recent_season}/schedules.json'  # API endpoint for schedules
    response = requests.get(schedules_url, params=params)  # Make the API request
    response.raise_for_status()  # Raise error for bad responses
    
    schedules_data = response.json().get('schedules', [])  # Parse JSON data from response
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
        for schedule in schedules_data  # Extract relevant fields from schedules data
    ]
    
    cache.set(cache_key, matches, CACHE_TIMEOUT)  # Store filtered data in cache
    return Response({'matches': matches})  # Return the data