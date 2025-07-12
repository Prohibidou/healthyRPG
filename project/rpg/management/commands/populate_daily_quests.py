from django.core.management.base import BaseCommand
from rpg.models import Quest, QuestType

class Command(BaseCommand):
    help = 'Populates the database with sample daily quests.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Populating daily quests...'))

        # Create QuestTypes if they don't exist
        exercise_type, _ = QuestType.objects.get_or_create(name='Exercise', defaults={'description': 'Quests related to physical activity.'})
        nutrition_type, _ = QuestType.objects.get_or_create(name='Nutrition', defaults={'description': 'Quests related to healthy eating.'})
        mind_type, _ = QuestType.objects.get_or_create(name='Mindfulness', defaults={'description': 'Quests related to mental well-being.'})

        quests_to_create = [
            {
                'name': 'Morning Stretch',
                'description': 'Perform 15 minutes of stretching exercises.',
                'xp_reward': 50,
                'quest_type': exercise_type,
                'time_of_day': 'Morning',
            },
            {
                'name': 'Hydration Hero',
                'description': 'Drink 8 glasses of water today.',
                'xp_reward': 30,
                'quest_type': nutrition_type,
                'time_of_day': 'Afternoon',
            },
            {
                'name': 'Mindful Minute',
                'description': 'Practice 5 minutes of meditation or deep breathing.',
                'xp_reward': 40,
                'quest_type': mind_type,
                'time_of_day': 'Night',
            },
            {
                'name': 'Walk the Plank',
                'description': 'Go for a 30-minute walk.',
                'xp_reward': 70,
                'quest_type': exercise_type,
                'time_of_day': 'Afternoon',
            },
            {
                'name': 'Veggie Victory',
                'description': 'Eat at least 3 servings of vegetables.',
                'xp_reward': 60,
                'quest_type': nutrition_type,
                'time_of_day': 'Morning',
            },
        ]

        for quest_data in quests_to_create:
            quest, created = Quest.objects.get_or_create(
                name=quest_data['name'],
                defaults={
                    'description': quest_data['description'],
                    'xp_reward': quest_data['xp_reward'],
                    'quest_type': quest_data['quest_type'],
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created quest: {quest.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Quest already exists: {quest.name}'))

        self.stdout.write(self.style.SUCCESS('Finished populating daily quests.'))
