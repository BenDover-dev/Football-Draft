# fetch_players.py
# A custom Django management command that fetches real player data
# from the official FPL (Fantasy Premier League) API and saves it
# to our PostgreSQL database.
#
# Run this command with: python manage.py fetch_players
#
# API used: https://fantasy.premierleague.com/api/bootstrap-static/
# This is a free public API — no key or signup required!
#
# What it does:
#   1. Fetches all 825 Premier League players from FPL API
#   2. Maps team IDs to team names
#   3. Maps position IDs to position codes (GK, DEF, MID, FWD)
#   4. Clears old player data and saves fresh data to the database

import requests
from django.core.management.base import BaseCommand
from players.models import Player

class Command(BaseCommand):
    help = 'Fetch players from FPL API'

    def handle(self, *args, **kwargs):
        self.stdout.write('Fetching players from FPL API...')
        
        # FPL public API endpoint — returns all players, teams and game data
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        response = requests.get(url)
        data = response.json()
        
        players = data['elements']  # List of all players
        
        # Map team ID to team name e.g. {1: 'Arsenal', 2: 'Aston Villa'}
        teams = {team['id']: team['name'] for team in data['teams']}
        
        # Map position ID to position code e.g. {1: 'GK', 2: 'DEF'}
        positions = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}
        
        # Clear old data before saving fresh data — keeps database clean
        Player.objects.all().delete()
        
        for player in players:
            Player.objects.create(
                name=f"{player['first_name']} {player['second_name']}",
                position=positions[player['element_type']],
                team=teams[player['team']],
                price=player['now_cost'] / 10,  # FPL stores price as integer e.g. 103 = £10.3m
                form=float(player['form'] or 0),
                total_points=player['total_points'],
                draft_score=0.0,
                photo=player['photo'].replace('.jpg', '')  # Remove extension for URL building
            )
        
        self.stdout.write(f'Successfully fetched {len(players)} players!')