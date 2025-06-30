from django.contrib import admin
from .models import (
    Quest,
    PlayerQuest,
    Achievement,
    PlayerAchievement
)

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_reward', 'quest_type', 'nutritional_archetype_quest', 'physical_archetype_quest', 'is_spiritual_quest')
    list_filter = ('quest_type', 'nutritional_archetype_quest', 'physical_archetype_quest', 'is_spiritual_quest')
    search_fields = ('name', 'description')

@admin.register(PlayerQuest)
class PlayerQuestAdmin(admin.ModelAdmin):
    list_display = ('player', 'quest', 'date_assigned', 'is_completed')
    list_filter = ('date_assigned', 'is_completed')
    search_fields = ('player__user__username', 'quest__name')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PlayerAchievement)
class PlayerAchievementAdmin(admin.ModelAdmin):
    list_display = ('player', 'achievement', 'date_unlocked')
    list_filter = ('date_unlocked',)
    search_fields = ('player__user__username', 'achievement__name')