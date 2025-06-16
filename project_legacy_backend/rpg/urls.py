from django.urls import path
from .views import CharacterDataView, DailyQuestsView, CompleteQuestView

urlpatterns = [
    path('character/',            CharacterDataView.as_view(), name='character-data'),
    path('quests/daily/',         DailyQuestsView.as_view(),   name='daily-quests'),
    path('quests/complete/<int:quest_id>/', CompleteQuestView.as_view(), name='complete-quest'),
]