from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath

class Command(BaseCommand):
    help = 'Creates or updates a Player profile for a specified user'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to set up')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" not found.'))
            return

        player, created = Player.objects.get_or_create(user=user)

        if created:
            self.stdout.write(self.style.SUCCESS(f'Player profile created for {username}.'))
        else:
            self.stdout.write(f'Player profile for {username} already exists.')

        # Assign default archetypes and path
        try:
            player.nutritional_archetype = NutritionalArchetype.objects.first()
            player.physical_archetype = PhysicalArchetype.objects.first()
            player.spiritual_path = SpiritualPath.objects.first()
            player.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully set up archetypes and path for player {username}.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error assigning archetypes: {e}'))
            self.stdout.write(self.style.WARNING('Please ensure you have created at least one of each archetype and spiritual path.'))
