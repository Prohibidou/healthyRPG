from rest_framework import serializers
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath
from .models import PlayerQuest

class NutritionalArchetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NutritionalArchetype
        fields = '__all__'

class PhysicalArchetypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhysicalArchetype
        fields = '__all__'

class SpiritualPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpiritualPath
        fields = '__all__'

class PlayerSerializer(serializers.ModelSerializer):
    nutritional_archetype = NutritionalArchetypeSerializer(allow_null=True)
    physical_archetype = PhysicalArchetypeSerializer(allow_null=True)
    # spiritual_path = SpiritualPathSerializer(allow_null=True)
    class Meta:
        model = Player
        fields = ('level', 'xp', 'nutritional_archetype', 'physical_archetype') #, 'spiritual_path')

class PlayerQuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerQuest
        fields = '__all__'
