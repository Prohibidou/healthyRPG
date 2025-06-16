from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Character, Quest, DailyLog
from .serializers import CharacterSerializer

def get_daily_quests_for_character(character):
    # TODO: reemplaza con tu lógica de generación basada en arquetipos
    return Quest.objects.all()[:5]


class CharacterDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            char = Character.objects.get(user=request.user)
        except Character.DoesNotExist:
            return Response({"error": "Character not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(CharacterSerializer(char).data)


class DailyQuestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        character = Character.objects.get(user=request.user)
        daily_quests = get_daily_quests_for_character(character)
        today = timezone.now().date()
        done_ids = DailyLog.objects.filter(
            character=character, completion_date=today
        ).values_list('quest_id', flat=True)

        data = []
        for q in daily_quests:
            data.append({
                'id':          q.id,
                'name':        q.name,
                'description': q.description,
                'xp_value':    q.xp_value,
                'is_completed': q.id in done_ids
            })
        return Response(data)


class CompleteQuestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, quest_id):
        character = Character.objects.get(user=request.user)
        try:
            quest = Quest.objects.get(pk=quest_id)
        except Quest.DoesNotExist:
            return Response({"error": "Quest not found"}, status=status.HTTP_404_NOT_FOUND)

        log, created = DailyLog.objects.get_or_create(
            character=character,
            quest=quest,
            completion_date=timezone.now().date()
        )
        if created:
            character.xp += quest.xp_value
            character.save()
            return Response({"message": f"Quest '{quest.name}' completed! +{quest.xp_value} XP."})
        return Response({"message": "Already completed today."}, status=status.HTTP_400_BAD_REQUEST)
