# serializers.py
# Converts Player model data into JSON format so the Vue frontend
# can read and display it. Think of it as a translator between
# the database and the frontend.
# Uses ModelSerializer which automatically handles all fields — DRY principle!

from rest_framework import serializers
from .models import Player

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player          # Which model to serialize
        fields = '__all__'      # Include all fields from the Player model