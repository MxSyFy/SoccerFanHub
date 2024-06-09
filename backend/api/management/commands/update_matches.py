from django.core.management.base import BaseCommand
from api.utils import update_matches, get_competitions, get_seasons_for_competition, get_most_recent_season

class Command(BaseCommand):
    help = 'Update matches from Sportradar API'

    def handle(self, *args, **kwargs):
        competitions = get_competitions()
        # Chose the first competition
        competition_id = competitions['competitions'][0]['id']
        seasons = get_seasons_for_competition(competition_id)
        most_recent_season = get_most_recent_season(seasons)
        season_id = most_recent_season['id']
        update_matches(season_id)
        self.stdout.write(self.style.SUCCESS('Successfully updated matches for season %s' % season_id))
