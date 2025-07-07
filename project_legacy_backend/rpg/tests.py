from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath
from rpg.models import Quest, PlayerQuest, QuestType

class QuestFilteringTests(TestCase):

    def setUp(self):
        # Create a user and player for testing
        self.user = User.objects.create_user(username='testuser', password='password')
        self.nutritional_archetype = NutritionalArchetype.objects.create(name='Balanced', description='Balanced diet')
        self.physical_archetype = PhysicalArchetype.objects.create(name='Strength', description='Strength training')
        self.spiritual_path = SpiritualPath.objects.create(name='Mindfulness', description='Mindfulness meditation')
        self.player = Player.objects.create(
            user=self.user,
            level=1,
            xp=0,
            nutritional_archetype=self.nutritional_archetype,
            physical_archetype=self.physical_archetype,
            spiritual_path=self.spiritual_path
        )

        # Create some quests for testing
        self.exercise_type = QuestType.objects.create(name='Exercise', description='Quests related to physical activity.')
        self.nutrition_type = QuestType.objects.create(name='Nutrition', description='Quests related to healthy eating.')
        self.mind_type = QuestType.objects.create(name='Mindfulness', description='Quests related to mental well-being.')

        Quest.objects.create(name='Morning Run', description='Run for 15 minutes.', xp_reward=20, quest_type=self.exercise_type, time_of_day='Morning')
        Quest.objects.create(name='Healthy Lunch', description='Eat a healthy lunch.', xp_reward=15, quest_type=self.nutrition_type, time_of_day='Afternoon')
        Quest.objects.create(name='Evening Meditation', description='Meditate for 10 minutes.', xp_reward=10, quest_type=self.mind_type, time_of_day='Night')

    def test_morning_quests(self):
        """Test that only morning quests are returned during the morning."""
        # Set the time to morning (e.g., 9 AM)
        with self.settings(TIME_ZONE='UTC'):
            now = timezone.now().replace(hour=9)
            with timezone.override(now):
                response = self.client.get('/rpg/api/quests/daily/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]['quest']['time_of_day'], 'Morning')

    def test_afternoon_quests(self):
        """Test that only afternoon quests are returned during the afternoon."""
        # Set the time to afternoon (e.g., 2 PM)
        with self.settings(TIME_ZONE='UTC'):
            now = timezone.now().replace(hour=14)
            with timezone.override(now):
                response = self.client.get('/rpg/api/quests/daily/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]['quest']['time_of_day'], 'Afternoon')

    def test_night_quests(self):
        """Test that only night quests are returned during the night."""
        # Set the time to night (e.g., 9 PM)
        with self.settings(TIME_ZONE='UTC'):
            now = timezone.now().replace(hour=21)
            with timezone.override(now):
                response = self.client.get('/rpg/api/quests/daily/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(len(response.data), 1)
                self.assertEqual(response.data[0]['quest']['time_of_day'], 'Night')