# api/views.py

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
import time

API_KEY = '4Iz53uKY8MaQs8q54t85Q9InTfObDj984WFONWTn'
BASE_URL = 'https://api.sportradar.com/soccer/trial/v4/en/'

def make_request(url):
    headers = {'Accept': 'application/json'}
    params = {'api_key': API_KEY}
    retries = 3
    delay = 1

    while retries > 0:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            time.sleep(delay)
            delay *= 2
            retries -= 1
        else:
            return None
    return None

@api_view(['GET'])
def get_competitions(request):
    url = f'{BASE_URL}/competitions.json'
    data = make_request(url)
    
    if not data:
        return Response({'error': 'Failed to retrieve competitions'}, status=500)

    competitions = [
        {
            'id': comp['id'],
            'name': comp['name'],
            'gender': comp['gender'],
            'category': comp['category'],
        }
        for comp in data.get('competitions', [])
        if comp.get('gender') == 'women'
    ]
    
    return Response({'competitions': competitions})

@api_view(['GET'])
def get_competitors(request, competition_id):
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
    data = make_request(seasons_url)
    
    if not data or not data.get('seasons'):
        return Response({'error': 'No seasons found for this competition'}, status=404)

    seasons = data['seasons']
    seasons.sort(key=lambda x: x['start_date'], reverse=True)
    most_recent_season = seasons[0]['id']
    competitors_url = f'{BASE_URL}/seasons/{most_recent_season}/competitors.json'
    competitors_data = make_request(competitors_url)

    if not competitors_data:
        return Response({'error': 'Failed to retrieve competitors'}, status=500)

    competitors = [
        {
            'id': competitor['id'],
            'name': competitor['name'],
            'country': competitor.get('country'),
            'abbreviation': competitor.get('abbreviation'),
            'gender': competitor.get('gender')
        }
        for competitor in competitors_data.get('season_competitors', [])
    ]

    return Response({'competitors': competitors})

@api_view(['GET'])
def get_matches(request, competition_id):
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
    data = make_request(seasons_url)

    if not data or not data.get('seasons'):
        return Response({'error': 'No seasons found for this competition'}, status=404)

    seasons = data['seasons']
    seasons.sort(key=lambda x: x['start_date'], reverse=True)
    most_recent_season = seasons[0]['id']
    schedules_url = f'{BASE_URL}/seasons/{most_recent_season}/schedules.json'
    schedules_data = make_request(schedules_url)

    if not schedules_data:
        return Response({'error': 'Failed to retrieve matches'}, status=500)

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
        for schedule in schedules_data.get('schedules', [])
    ]

    return Response({'matches': matches})
