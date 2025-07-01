from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from legacy_core.models import Player

class Command(BaseCommand):
    help = 'Creates a player profile for a user who does not have one'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username of the user to create a player profile for')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            if not Player.objects.filter(user=user).exists():
                Player.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created player profile for {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'Player profile for {username} already exists'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User with username {username} does not exist'))
