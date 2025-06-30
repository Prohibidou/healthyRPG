from django.contrib.auth.models import User
from legacy_core.models import Player, NutritionalArchetype, PhysicalArchetype, SpiritualPath

user = User.objects.get(username='admin')
player, created = Player.objects.get_or_create(user=user)

if created:
    print('Player profile created for admin.')
else:
    print('Player profile for admin already existed.')

# Assign default archetypes and path
player.nutritional_archetype = NutritionalArchetype.objects.first()
player.physical_archetype = PhysicalArchetype.objects.first()
player.spiritual_path = SpiritualPath.objects.first()
player.save()

print('Player profile for admin is set up.')
