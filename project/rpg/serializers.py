from rest_framework import serializers
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath
from .models import PlayerQuest, Quest, QuestType # Import Quest and QuestType

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

class QuestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestType
        fields = '__all__'

class QuestSerializer(serializers.ModelSerializer):
    quest_type = QuestTypeSerializer(read_only=True) # Nested serializer for QuestType
    class Meta:
        model = Quest
        fields = ('id', 'name', 'description', 'xp_reward', 'quest_type') # Include quest_type

class PlayerQuestSerializer(serializers.ModelSerializer):
    quest = QuestSerializer(read_only=True) # Nested serializer for Quest
    class Meta:
        model = PlayerQuest
        fields = ('id', 'quest', 'date_assigned', 'is_completed') # Include quest details