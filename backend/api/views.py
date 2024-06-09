# api/veiws.py

from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import TeamSerializer, MatchSerializer
from .models import Team, Match

class TeamView(APIView):

    def get(self, request, pk=None):
        if pk:
            team = get_object_or_404(Team.objects.all(), pk=pk)
            serializer = TeamSerializer(team)
        else:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request):
        team = request.data
        serializer = TeamSerializer(data=team)
        if serializer.is_valid(raise_exception=True):
            team_saved = serializer.save()
        return Response({"result": f"Team {team_saved.teamName} saved"})

    def put(self, request, pk):
        saved_team = get_object_or_404(Team.objects.all(), pk=pk)
        data = request.data
        serializer = TeamSerializer(instance=saved_team, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            team_saved = serializer.save()
        return Response({"result": f"Team {team_saved.teamName} updated"})

    def delete(self, request, pk):
        team = get_object_or_404(Team.objects.all(), pk=pk)
        team.delete()
        return Response({"result": f"Team id {pk} deleted"}, status=204)


class MatchView(APIView):

    def get(self, request, pk=None):
        if pk:
            match = get_object_or_404(Match.objects.all(), pk=pk)
            serializer = MatchSerializer(match)
        else:
            matches = Match.objects.all()
            serializer = MatchSerializer(matches, many=True)
        return Response(serializer.data)

    def post(self, request):
        match = request.data
        serializer = MatchSerializer(data=match)
        if serializer.is_valid(raise_exception=True):
            match_saved = serializer.save()
        return Response({"result": f"Match {match_saved.id} saved"})

    def put(self, request, pk):
        saved_match = get_object_or_404(Match.objects.all(), pk=pk)
        data = request.data
        serializer = MatchSerializer(instance=saved_match, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            match_saved = serializer.save()
        return Response({"result": f"Match {match_saved.id} updated"})

    def delete(self, request, pk):
        match = get_object_or_404(Match.objects.all(), pk=pk)
        match.delete()
        return Response({"result": f"Match id {pk} deleted"}, status=204)
