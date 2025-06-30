import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legacy_core.settings')
django.setup()

from django.contrib.auth.models import User
from legacy_core.models import Player

username = "maxi"

try:
    user = User.objects.get(username=username)
    if not Player.objects.filter(user=user).exists():
        Player.objects.create(user=user)
        print(f"Successfully created player profile for '{username}'.")
    else:
        print(f"Player profile for '{username}' already exists.")
except User.DoesNotExist:
    print(f"User with username '{username}' does not exist.")
