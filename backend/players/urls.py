# urls.py (players app)
# Defines the URL routes for the players API.
# Uses Django REST Framework's DefaultRouter which automatically
# generates the following endpoints:
#   GET  /api/players/     — list all players
#   POST /api/players/     — create a new player
#   GET  /api/players/{id} — get a specific player
#   PUT  /api/players/{id} — update a specific player
#   DEL  /api/players/{id} — delete a specific player

from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet

router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')

urlpatterns = router.urls