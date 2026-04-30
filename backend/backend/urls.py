# urls.py (root — backend project)
# Main URL configuration for the Django project.
# Routes all incoming requests to the correct app.
#   /admin/           — Django admin panel
#   /api/players/     — Players API (CRUD via PlayerViewSet)
#   /api/auth/...     — Auth endpoints (register, login, forgot/reset password, news)

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('players.urls')),
    path('api/auth/', include('accounts.urls')),
]