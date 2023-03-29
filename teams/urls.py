from django.urls import path

from .views import list_teams, create_team

urlpatterns = [
    path("api/teams/", list_teams, name="list-teams"),
    path("api/teams/", create_team, name="create-team"),
]
