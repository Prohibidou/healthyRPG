from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a test user for development'

    def handle(self, *args, **options):
        username = 'testuser'
        password = 'testpassword'
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, password=password, email='test@example.com')
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        else:
            self.stdout.write(self.style.WARNING(f'User {username} already exists.'))
