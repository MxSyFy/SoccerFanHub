# api/management/commands/update_teams.py

from django.core.management.base import BaseCommand
from api.utils import update_teams

class Command(BaseCommand):
    help = 'Update teams from Sportradar API'

    def handle(self, *args, **kwargs):
        update_teams()
        self.stdout.write(self.style.SUCCESS('Successfully updated teams'))
