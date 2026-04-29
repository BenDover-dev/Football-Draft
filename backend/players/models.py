# models.py
# Defines the Player model — this is the blueprint for how a player
# is stored in the PostgreSQL database. Every field here becomes
# a column in the players_player table.

from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)        # Full name of the player
    position = models.CharField(max_length=10)     # GK, DEF, MID, or FWD
    team = models.CharField(max_length=100)        # Club name e.g. Arsenal
    price = models.FloatField()                    # Price in millions e.g. 10.3
    form = models.FloatField()                     # Recent form score from FPL
    total_points = models.IntegerField(default=0)  # Total FPL points this season
    draft_score = models.FloatField(default=0.0)   # Our calculated ranking score
    photo = models.CharField(max_length=100, blank=True, default='')  # FPL photo code

    def __str__(self):
        return self.name  # Shows player name in admin and terminal