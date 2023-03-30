from django.urls import path
from .views import TeamListCreateView, TeamIdentifierView

urlpatterns = [
    path("teams/", TeamListCreateView.as_view()),
    path("teams/<int:id>/", TeamIdentifierView.as_view()),
]
