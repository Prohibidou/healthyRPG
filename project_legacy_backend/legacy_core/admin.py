from django.contrib import admin
from .models import (
    Player, 
    NutritionalArchetype, 
    PhysicalArchetype, 
    SpiritualPath
)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'nutritional_archetype', 'physical_archetype', 'spiritual_path')
    list_filter = ('nutritional_archetype', 'physical_archetype', 'spiritual_path')
    search_fields = ('user__username',)

@admin.register(NutritionalArchetype)
class NutritionalArchetypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(PhysicalArchetype)
class PhysicalArchetypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(SpiritualPath)
class SpiritualPathAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)