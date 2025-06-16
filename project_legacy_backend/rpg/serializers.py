from rest_framework import serializers
from .models import Character

class CharacterSerializer(serializers.ModelSerializer):
    nutritional_archetype_name = serializers.CharField(source='get_nutritional_archetype_display')
    physical_archetype_name    = serializers.CharField(source='get_physical_archetype_display')
    spiritual_path_name        = serializers.CharField(source='get_spiritual_path_display')

    class Meta:
        model  = Character
        fields = [
            'name', 'level', 'xp',
            'nutritional_archetype_name',
            'physical_archetype_name',
            'spiritual_path_name',
            'login_streak', 'spiritual_streak'
        ]
