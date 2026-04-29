# admin.py
# Registers the Player model with Django's built-in admin dashboard.
# This allows you to view, add, edit and delete players directly
# through the admin interface at http://127.0.0.1:8000/admin/
#
# To access the admin dashboard you need a superuser account.
# Create one with: python manage.py createsuperuser

from django.contrib import admin
from .models import Player

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    # Columns to show in the player list in admin
    list_display = ['name', 'position', 'team', 'price', 'form', 'total_points', 'draft_score']
    
    # Add filters on the right side of the admin list
    list_filter = ['position', 'team']
    
    # Enable search by player name and team
    search_fields = ['name', 'team']