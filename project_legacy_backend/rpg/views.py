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
import pytz

from legacy_core.models import Player
from .models import Quest, PlayerQuest
from .serializers import PlayerSerializer, PlayerQuestSerializer

from rest_framework.authentication import TokenAuthentication

from rest_framework.permissions import IsAuthenticated, AllowAny

class PlayerProfileView(APIView):
    """
    Devuelve el perfil completo del jugador autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        player = get_object_or_404(Player, user=request.user)
        serializer = PlayerSerializer(player)
        return Response(serializer.data)

class DailyQuestsView(APIView):
    """
    Obtiene o crea las misiones diarias para el jugador.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_timezone_str = request.headers.get('X-User-Timezone')
        now = timezone.now()

        if user_timezone_str:
            try:
                import pytz
                user_timezone = pytz.timezone(user_timezone_str)
                now = now.astimezone(user_timezone)
            except pytz.UnknownTimeZoneError:
                pass  # Handle invalid timezone gracefully

        current_hour = now.hour
        today = now.date()

        if 5 <= current_hour < 12:
            time_of_day = 'Morning'
        elif 12 <= current_hour < 17:
            time_of_day = 'Afternoon'
        else:
            time_of_day = 'Night'

        player = get_object_or_404(Player, user=request.user)
        
        player_quests = PlayerQuest.objects.filter(
            player=player, 
            date_assigned=today, 
            quest__time_of_day=time_of_day
        )

        if not player_quests.exists():
            quests_to_assign = Quest.objects.filter(time_of_day=time_of_day)
            
            new_player_quests = []
            for quest in quests_to_assign:
                pq = PlayerQuest(player=player, quest=quest, date_assigned=today)
                new_player_quests.append(pq)
            
            if new_player_quests:
                PlayerQuest.objects.bulk_create(new_player_quests)
                player_quests = PlayerQuest.objects.filter(
                    player=player, 
                    date_assigned=today, 
                    quest__time_of_day=time_of_day
                )

        serializer = PlayerQuestSerializer(player_quests, many=True)
        return Response(serializer.data)

class CompleteQuestView(APIView):
    """
    Marca una misión diaria como completada.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, player_quest_id):
        player = get_object_or_404(Player, user=request.user)
        player_quest = get_object_or_404(PlayerQuest, id=player_quest_id, player=player)

        if not player_quest.is_completed:
            player_quest.is_completed = True
            player_quest.save()
            player.add_xp(player_quest.quest.xp_reward)

        return Response({
            "message": f"Quest {player_quest.quest.name} marked as complete!",
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
        
        user_timezone_str = self.request.headers.get('X-User-Timezone')

        now = timezone.now()

        if user_timezone_str:
            try:
                user_timezone = pytz.timezone(user_timezone_str)
                now = now.astimezone(user_timezone)
            except pytz.UnknownTimeZoneError:
                # Handle invalid timezone gracefully
                pass

        current_hour = now.hour

        if 5 <= current_hour < 12:
            time_of_day = 'Morning'
        elif 12 <= current_hour < 17:
            time_of_day = 'Afternoon'
        else:
            time_of_day = 'Night'

        player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today, quest__time_of_day=time_of_day)
        if not player_quests.exists():
            nutritional_quests = Quest.objects.filter(nutritional_archetype_quest=player.nutritional_archetype, time_of_day=time_of_day)
            physical_quests = Quest.objects.filter(physical_archetype_quest=player.physical_archetype, time_of_day=time_of_day)
            spiritual_quest = Quest.objects.filter(is_spiritual_quest=True, time_of_day=time_of_day)
            all_quests = list(nutritional_quests) + list(physical_quests) + list(spiritual_quest)
            new_player_quests = []
            for quest in all_quests:
                pq = PlayerQuest(player=player, quest=quest, date_assigned=today)
                new_player_quests.append(pq)
            PlayerQuest.objects.bulk_create(new_player_quests)
            player_quests = PlayerQuest.objects.filter(player=player, date_assigned=today, quest__time_of_day=time_of_day)
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
