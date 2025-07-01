from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from legacy_core.models import Player

@receiver(user_signed_up)
def create_player_profile(sender, **kwargs):
    user = kwargs.pop('user')
    Player.objects.create(user=user)
