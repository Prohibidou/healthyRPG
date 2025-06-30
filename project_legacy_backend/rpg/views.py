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

class PlayerProfileView(APIView):
    """
    Devuelve el perfil completo del jugador autenticado.
    """
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            player = Player.objects.get(user=request.user)
            serializer = PlayerSerializer(player)
            return Response(serializer.data)
        except Player.DoesNotExist:
            return Response({
                "error": "Player profile not found for this user.",
                "user_searched": request.user.username
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Print the full traceback to the console
            traceback.print_exc()
            return Response({
                "error": "An unexpected error occurred. Check the server console for details.",
                "details": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DailyQuestsView(APIView):
    """
    Obtiene o crea las misiones diarias para el jugador.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user)
        today = timezone.now().date()

        # 1. Buscar misiones ya asignadas para hoy.
        player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today)

        # 2. Si no hay, crearlas.
        if not player_quests.exists():
            # Misiones fundamentales de arquetipos
            nutritional_quests = Quest.objects.filter(nutritional_archetype_quest=player.nutritional_archetype)
            physical_quests = Quest.objects.filter(physical_archetype_quest=player.physical_archetype)
            # Misión espiritual diaria
            spiritual_quest = Quest.objects.filter(is_spiritual_quest=True)

            # Combinar todas las misiones y crear las instancias para el jugador
            all_quests = list(nutritional_quests) + list(physical_quests) + list(spiritual_quest)
            
            new_player_quests = []
            for quest in all_quests:
                pq = PlayerQuest(player=player, quest=quest, date_assigned=today)
                new_player_quests.append(pq)
            
            PlayerQuest.objects.bulk_create(new_player_quests)
            
            # Volver a consultar para obtener la lista fresca
            player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today)

        serializer = PlayerQuestSerializer(player_quests, many=True)
        return Response(serializer.data)

class CompleteQuestView(APIView):
    """
    Marca una misión diaria como completada.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_quest_id):
        player = get_object_or_404(Player, user=request.user)
        
        # Buscamos la misión asignada específica por su ID
        player_quest = get_object_or_404(PlayerQuest, id=player_quest_id, player=player)

        if player_quest.is_completed:
            return Response({"message": "Misión ya completada."}, status=status.HTTP_400_BAD_REQUEST)

        # Marcar como completada y dar recompensa
        player_quest.is_completed = True
        player_quest.save()

        # Añadir XP al jugador
        player.add_xp(player_quest.quest.xp_reward)

        return Response({
            "message": f"¡Misión '{player_quest.quest.title}' completada!",
            "xp_gained": player_quest.quest.xp_reward,
            "current_xp": player.xp,
            "current_level": player.level
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
