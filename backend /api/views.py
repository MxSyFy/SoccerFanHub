# api/views.py

from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests

# Sportradar API key and base URL
API_KEY = '4Iz53uKY8MaQs8q54t85Q9InTfObDj984WFONWTn'
BASE_URL = 'https://api.sportradar.com/soccer/trial/v4/en/'

@api_view(['GET'])
def get_competitions(request):
    # Endpoint URL for fetching competitions
    url = f'{BASE_URL}/competitions.json'
    headers = {'Accept': 'application/json'}
    params = {'api_key': API_KEY}

    # Make a GET request to fetch competitions data
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        # Handle request failure
        return Response({'error': 'Failed to retrieve competitions'}, status=response.status_code)

    # Parse the JSON response
    data = response.json()

    # Filter competitions where gender is 'women'
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

    # Return filtered competitions
    return Response({'competitions': filtered_competitions})

@api_view(['GET'])
def get_competitors(request, competition_id):
    # Endpoint URL to fetch seasons for a specific competition
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
    headers = {'Accept': 'application/json'}
    params = {'api_key': API_KEY}

    # Make a GET request to fetch seasons data
    response = requests.get(seasons_url, headers=headers, params=params)
    if response.status_code != 200:
        # Handle request failure
        return Response({'error': 'Failed to retrieve competitors'}, status=response.status_code)

    # Parse the JSON response
    data = response.json()

    # Sort seasons by start date in descending order
    data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)

    # Get the ID of the most recent season
    most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None

    if not most_recent_season:
        # Handle no seasons found for the competition
        return Response({'error': 'No seasons found for this competition'}, status=404)

    # Endpoint URL to fetch competitors for the most recent season
    competitors_url = f'{BASE_URL}/seasons/{most_recent_season}/competitors.json'
    response = requests.get(competitors_url, headers=headers, params=params)
    if response.status_code != 200:
        # Handle request failure
        return Response({'error': 'Failed to retrieve competitors'}, status=response.status_code)

    # Parse competitors data from JSON response
    competitors_data = response.json().get('season_competitors', [])

    # Format competitors data
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

    # Return competitors data
    return Response({'competitors': competitors})

@api_view(['GET'])
def get_matches(request, competition_id):
    # Endpoint URL to fetch seasons for a specific competition
    seasons_url = f'{BASE_URL}/competitions/{competition_id}/seasons.json'
    headers = {'Accept': 'application/json'}
    params = {'api_key': API_KEY}

    # Make a GET request to fetch seasons data
    response = requests.get(seasons_url, headers=headers, params=params)
    if response.status_code != 200:
        # Handle request failure
        return Response({'error': 'Failed to retrieve matches'}, status=response.status_code)

    # Parse the JSON response
    data = response.json()

    # Sort seasons by start date in descending order
    data['seasons'].sort(key=lambda x: x['start_date'], reverse=True)

    # Get the ID of the most recent season
    most_recent_season = data['seasons'][0]['id'] if data['seasons'] else None

    if not most_recent_season:
        # Handle no seasons found for the competition
        return Response({'error': 'No seasons found for this competition'}, status=404)

    # Endpoint URL to fetch schedules/matches for the most recent season
    schedules_url = f'{BASE_URL}/seasons/{most_recent_season}/schedules.json'
    response = requests.get(schedules_url, headers=headers, params=params)
    if response.status_code != 200:
        # Handle request failure
        return Response({'error': 'Failed to retrieve matches'}, status=response.status_code)

    # Parse schedules/matches data from JSON response
    schedules_data = response.json().get('schedules', [])

    # Format matches data
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

    # Return matches data
    return Response({'matches': matches})
