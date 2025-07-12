from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath

class Command(BaseCommand):
    help = 'Creates or updates the Player profile for the admin user'

    def handle(self, *args, **options):
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('Admin user not found. Please create a superuser named "admin".'))
            return

        player, created = Player.objects.get_or_create(user=admin_user)

        if created:
            self.stdout.write(self.style.SUCCESS('Player profile created for admin.'))
        else:
            self.stdout.write('Player profile for admin already exists.')

        # Assign default archetypes and path
        try:
            player.nutritional_archetype = NutritionalArchetype.objects.first()
            player.physical_archetype = PhysicalArchetype.objects.first()
            player.spiritual_path = SpiritualPath.objects.first()
            player.save()
            self.stdout.write(self.style.SUCCESS('Successfully set up archetypes and path for admin player.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error assigning archetypes: {e}'))
            self.stdout.write(self.style.WARNING('Please ensure you have created at least one of each archetype and spiritual path.'))
