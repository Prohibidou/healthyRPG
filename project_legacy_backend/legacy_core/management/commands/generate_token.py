from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Generates or retrieves an authentication token for a given user.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='The username for which to generate the token.')

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            token, created = Token.objects.get_or_create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Token for user {username}: {token.key}'))
            if created:
                self.stdout.write(self.style.SUCCESS('Token was newly generated.'))
            else:
                self.stdout.write(self.style.SUCCESS('Token already existed.'))
        except User.DoesNotExist:
            self.stderr.write(self.style.ERROR(f'User with username "{username}" does not exist.'))
