from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from legacy_core.models import Player

class Command(BaseCommand):
    help = 'Creates a player profile for a given username if one does not already exist.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to create a player profile for.')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise CommandError(f'User with username "{username}" does not exist.')

        if Player.objects.filter(user=user).exists():
            self.stdout.write(self.style.SUCCESS(f'Player profile for "{username}" already exists.'))
            return

        Player.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS(f'Successfully created player profile for "{username}".'))
