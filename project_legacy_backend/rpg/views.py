import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from legacy_core.models import Player
from .models import Quest, PlayerQuest
from .serializers import PlayerSerializer, PlayerQuestSerializer

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated, AllowAny

class PlayerProfileView(APIView):
    """
    Devuelve el perfil completo del jugador autenticado.
    """
    permission_classes = [AllowAny]  # Allow any access for mock data

    def get(self, request):
        # Mock player data since we don't have a real user
        mock_player_data = {
            "level": 5,
            "xp": 1250,
            "nutritional_archetype": {"name": "Balanced"},
            "physical_archetype": {"name": "Strength"},
            "spiritual_path": {"name": "Mindfulness"}
        }
        return Response(mock_player_data)

class DailyQuestsView(APIView):
    """
    Obtiene o crea las misiones diarias para el jugador.
    """
    permission_classes = [AllowAny] # Allow any access for mock data

    def get(self, request):
        # Mock quest data
        mock_quests = [
            {
                "id": 1,
                "quest": {
                    "name": "Morning Jog",
                    "description": "Run for 15 minutes.",
                    "quest_type": {"name": "Physical"},
                    "xp_reward": 20
                },
                "is_completed": False
            },
            {
                "id": 2,
                "quest": {
                    "name": "Healthy Breakfast",
                    "description": "Eat a balanced breakfast.",
                    "quest_type": {"name": "Nutritional"},
                    "xp_reward": 15
                },
                "is_completed": False
            }
        ]
        return Response(mock_quests)

class CompleteQuestView(APIView):
    """
    Marca una misión diaria como completada.
    """
    permission_classes = [AllowAny] # Allow any access for mock data

    def post(self, request, player_quest_id):
        # In a real app, you'd update the database.
        # For this mock, we just return a success message.
        return Response({
            "message": f"Quest {player_quest_id} marked as complete!",
            "xp_gained": 15, # Mock XP
            "current_xp": 1265, # Mock total XP
            "current_level": 5
        })

class PlayerProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'rpg/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['player'] = get_object_or_404(Player, user=self.request.user)
        return context

class DailyQuestsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'rpg/quests.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = get_object_or_404(Player, user=self.request.user)
        today = timezone.now().date()
        player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today)
        if not player_quests.exists():
            nutritional_quests = Quest.objects.filter(nutritional_archetype_quest=player.nutritional_archetype)
            physical_quests = Quest.objects.filter(physical_archetype_quest=player.physical_archetype)
            spiritual_quest = Quest.objects.filter(is_spiritual_quest=True)
            all_quests = list(nutritional_quests) + list(physical_quests) + list(spiritual_quest)
            new_player_quests = []
            for quest in all_quests:
                pq = PlayerQuest(player=player, quest=quest, date_assigned=today)
                new_player_quests.append(pq)
            PlayerQuest.objects.bulk_create(new_player_quests)
            player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today)
        context['player_quests'] = player_quests
        return context

class CompleteQuestTemplateView(LoginRequiredMixin, APIView):
    def post(self, request, player_quest_id):
        player = get_object_or_404(Player, user=request.user)
        player_quest = get_object_or_404(PlayerQuest, id=player_quest_id, player=player)
        if not player_quest.is_completed:
            player_quest.is_completed = True
            player_quest.save()
            player.add_xp(player_quest.quest.xp_reward)
        return redirect('rpg:quests')
