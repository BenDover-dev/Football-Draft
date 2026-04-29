# views.py
# Handles API requests for player data.
# Calculates the draft score for each player using our ranking algorithm
# and returns the sorted list to the frontend.
#
# Draft Score Formula (KISS principle — simple weighted average):
#   Form Weight:   40% — recent performance matters most
#   Points Weight: 40% — total season points matters equally  
#   Value Weight:  20% — points per million spent

from rest_framework import viewsets
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