from rest_framework.test import APITestCase
from unittest.mock import patch
from django.utils import timezone
from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath
from rpg.models import Quest, PlayerQuest, QuestType

class QuestFilteringTests(APITestCase):

    def setUp(self):
        # Clear existing quests and player quests to ensure a clean state
        Quest.objects.all().delete()
        PlayerQuest.objects.all().delete()

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

        Quest.objects.create(name='Morning Jog', description='Run for 15 minutes.', xp_reward=20, quest_type=self.exercise_type, time_of_day='Morning')
        Quest.objects.create(name='Healthy Breakfast', description='Eat a healthy lunch.', xp_reward=15, quest_type=self.nutrition_type, time_of_day='Morning')
        Quest.objects.create(name='Walk the Plank', description='Go for a 30-minute walk.', xp_reward=70, quest_type=self.exercise_type, time_of_day='Afternoon')
        Quest.objects.create(name='Mindful Minute', description='Practice 5 minutes of meditation or deep breathing.', xp_reward=40, quest_type=self.mind_type, time_of_day='Night')

    @patch('rpg.views.timezone')
    def test_morning_quests(self, mock_timezone):
        """Test that only morning quests are returned during the morning."""
        # Set the time to morning (e.g., 9 AM)
        mock_timezone.now.return_value = timezone.now().replace(hour=9)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/rpg/api/quests/daily/')
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2, "Expected 2 morning quests.")
        for quest_data in response.data:
            self.assertEqual(quest_data['quest']['time_of_day'], 'Morning', "All returned quests should be morning quests.")

    @patch('rpg.views.timezone')
    def test_afternoon_quests(self, mock_timezone):
        """Test that only afternoon quests are returned during the afternoon."""
        # Set the time to afternoon (e.g., 2 PM)
        mock_timezone.now.return_value = timezone.now().replace(hour=14)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/rpg/api/quests/daily/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, "Expected 1 afternoon quest.")
        for quest_data in response.data:
            self.assertEqual(quest_data['quest']['time_of_day'], 'Afternoon', "All returned quests should be afternoon quests.")

    @patch('rpg.views.timezone')
    def test_night_quests(self, mock_timezone):
        """Test that only night quests are returned during the night."""
        # Set the time to night (e.g., 9 PM)
        mock_timezone.now.return_value = timezone.now().replace(hour=21)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/rpg/api/quests/daily/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1, "Expected 1 night quest.")
        for quest_data in response.data:
            self.assertEqual(quest_data['quest']['time_of_day'], 'Night', "All returned quests should be night quests.")