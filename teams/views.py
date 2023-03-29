from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import data_processing
from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError
from .models import Team


@api_view(["GET"])
def list_teams(request):
    try:
        data = {
            "titles": request.query_params.get("titles", 0),
            "first_cup": request.query_params.get("first_cup", ""),
        }
        data_processing(data)
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)
    except TeamException as err:
        return Response({"error": str(err)}, status=400)


@api_view(["POST"])
def create_team(request):
    try:
        data = data_processing(request.data)
        team = Team.objects.create(
            name=data["name"],
            titles=data["titles"],
            top_scorer=data["top_scorer"],
            fifa_code=data["fifa_code"],
            first_cup=data["first_cup"],
        )
        serializer = TeamSerializer(team)
        return Response(serializer.data, status=201)
    except TeamException as err:
        return Response({"error": str(err)}, status=400)
