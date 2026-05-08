# views.py
# Handles API requests for player data.
# Calculates the draft score for each player using our ranking algorithm
# and returns the sorted list to the frontend.
#
# Draft Score Formula (KISS principle — simple weighted average):
#   Form Weight:   40% — recent performance matters most
#   Points Weight: 40% — total season points matters equally  
#   Value Weight:  20% — points per million spent

import requests
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Player
from .serializers import PlayerSerializer

def calculate_draft_score(player):
    # Weights for each factor — must add up to 1.0 (100%)
    form_weight = 0.4
    points_weight = 0.4
    value_weight = 0.2

    # Calculate each component of the score
    form_score = float(player.form) * form_weight
    points_score = (player.total_points / 10) * points_weight
    value_score = (player.total_points / max(player.price, 1)) * value_weight

    # Return final score rounded to 2 decimal places
    return round(form_score + points_score + value_score, 2)

class PlayerViewSet(viewsets.ModelViewSet):
    # ModelViewSet automatically provides GET, POST, PUT, DELETE endpoints
    # DRY principle — no need to write each endpoint manually
    serializer_class = PlayerSerializer

    def get_queryset(self):
        # Fetch all players and calculate their draft score on the fly
        players = Player.objects.all()
        for player in players:
            player.draft_score = calculate_draft_score(player)
        return players


@api_view(['GET'])
def fetch_players_trigger(request):
    """One-time endpoint to populate the database with FPL players."""
    try:
        url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        response = requests.get(url, timeout=30)
        data = response.json()

        players = data['elements']
        teams = {team['id']: team['name'] for team in data['teams']}
        positions = {1: 'GK', 2: 'DEF', 3: 'MID', 4: 'FWD'}

        Player.objects.all().delete()
        for player in players:
            Player.objects.create(
                name=f"{player['first_name']} {player['second_name']}",
                position=positions[player['element_type']],
                team=teams[player['team']],
                price=player['now_cost'] / 10,
                form=float(player['form'] or 0),
                total_points=player['total_points'],
                draft_score=0.0,
                photo=player['photo'].replace('.jpg', '')
            )
        return Response({'status': 'success', 'players_fetched': len(players)})
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=500)