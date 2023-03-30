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
        return Response(teams_dict, status=200)

    def post(self, request):
        team_data = request.data

        try:
            data_processing(team_data)
        except (NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError) as err:
            return Response({"error": err.message}, status=400)

        team = Team.objects.create(**request.data)

        response_data = model_to_dict(team)

        return Response(response_data, status=201)


class TeamIdentifierView(APIView):
    def get(self, _, id):
        try:
            team = Team.objects.get(id=id)

            return Response(model_to_dict(team), status=200)
        
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status=404)

    def delete(self, _, id):
        try:
            team = Team.objects.get(id=id)
            team.delete()

            return Response(status=204)
        
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status=404)

    def patch(self, request, id):
        try:
            team = Team.objects.get(id=id)
            team.__dict__.update(request.data)
            team.save()

            return Response(model_to_dict(team), status=200)
        
        except Team.DoesNotExist:
            return Response({"message": "Team not found"}, status=404)
