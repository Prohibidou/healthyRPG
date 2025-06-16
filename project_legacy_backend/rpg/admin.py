from django.contrib import admin
from django.contrib import admin
from .models import Character, Quest, DailyLog

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'level', 'xp', 'nutritional_archetype', 'physical_archetype', 'spiritual_path')
    list_filter  = ('nutritional_archetype', 'physical_archetype', 'spiritual_path')
    search_fields = ('name', 'user__username')

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = ('name', 'xp_value')
    search_fields = ('name',)

@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('character', 'quest', 'completion_date')
    list_filter  = ('completion_date',)

# Register your models here.
