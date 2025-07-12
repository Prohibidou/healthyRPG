from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath

class Command(BaseCommand):
    help = 'Creates a test user with a complete player profile for development'

    def handle(self, *args, **options):
        username = 'testuser'
        password = 'testpassword'

        if not User.objects.filter(username=username).exists():
            # Create the user
            user = User.objects.create_user(username=username, password=password, email='test@example.com')
            self.stdout.write(self.style.SUCCESS(f'Successfully created user: {username}'))

            # Ensure default archetypes and paths exist
            nutritional_archetype, _ = NutritionalArchetype.objects.get_or_create(
                name='Balanced', 
                defaults={'description': 'A balanced diet for all-around sailors.'}
            )
            physical_archetype, _ = PhysicalArchetype.objects.get_or_create(
                name='Strength', 
                defaults={'description': 'Builds muscle for hauling the mainsail.'}
            )
            spiritual_path, _ = SpiritualPath.objects.get_or_create(
                name='Mindfulness', 
                defaults={'description': 'Keeps a clear head in stormy seas.'}
            )

            # Create the player profile and link it to the user
            Player.objects.create(
                user=user,
                level=1,
                xp=0,
                nutritional_archetype=nutritional_archetype,
                physical_archetype=physical_archetype,
                spiritual_path=spiritual_path
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created player profile for {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
