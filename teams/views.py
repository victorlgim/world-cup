from django.forms import ValidationError, model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Team
from .utils import data_processing
from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError


class TeamListCreateView(APIView):
    def get(self, _):
        teams = Team.objects.all()
        teams_dict = []

        for team in teams:
            dict_team = model_to_dict(team)
            teams_dict.append(dict_team)
        return Response(teams_dict)

    def post(self, request):
        team_data = request.data

        try:
            validated_data = data_processing(team_data)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as e:
            return Response({'error': e.message}, 400)

        team = Team.objects.create(
            name=validated_data["name"],
            titles=validated_data["titles"],
            top_scorer=validated_data["top_scorer"],
            fifa_code=validated_data["fifa_code"],
            first_cup=validated_data["first_cup"],
        )

        response_data = model_to_dict(team)

        return Response(response_data, 201)
