
from django.urls import path
from .views import (
    PlayerProfileView, 
    DailyQuestsView, 
    CompleteQuestView,
    PlayerProfileTemplateView,
    DailyQuestsTemplateView,
    CompleteQuestTemplateView,
    LoginView
)

app_name = 'rpg'

urlpatterns = [
    # API Views
    path('api/profile/', PlayerProfileView.as_view(), name='player-profile-api'),
    path('api/quests/daily/', DailyQuestsView.as_view(), name='daily-quests-api'),
    path('api/quests/complete/<int:player_quest_id>/', CompleteQuestView.as_view(), name='complete-quest-api'),

    # Template Views
    path('profile/', PlayerProfileTemplateView.as_view(), name='profile'),
    path('quests/', DailyQuestsTemplateView.as_view(), name='quests'),
    path('quests/complete/<int:player_quest_id>/', CompleteQuestTemplateView.as_view(), name='complete-quest-view'),
    path('login/', LoginView.as_view(), name='login'),
]
