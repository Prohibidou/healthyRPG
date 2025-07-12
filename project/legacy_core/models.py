
from django.db import models
from django.contrib.auth.models import User

class NutritionalArchetype(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class PhysicalArchetype(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class SpiritualPath(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    nutritional_archetype = models.ForeignKey(NutritionalArchetype, on_delete=models.SET_NULL, null=True, blank=True)
    physical_archetype = models.ForeignKey(PhysicalArchetype, on_delete=models.SET_NULL, null=True, blank=True)
    spiritual_path = models.ForeignKey(SpiritualPath, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

    def add_xp(self, amount):
        self.xp += amount
        self.check_level_up()
        self.save()

    def check_level_up(self):
        # Example: level up every 100 XP
        xp_to_level_up = self.level * 100
        if self.xp >= xp_to_level_up:
            self.level += 1
            self.xp -= xp_to_level_up
            # You might want to add a notification or other logic here
            self.check_level_up() # Check if another level up is warranted
