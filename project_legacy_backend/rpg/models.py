from django.db import models
from django.db import models
from django.contrib.auth.models import User

class Character(models.Model):
    class NutritionalArchetype(models.TextChoices):
        FITNESS   = 'FIT', 'Perfil Fitness'
        ANCESTRAL = 'ANC', 'Guerrero Ancestral'
        DRUID     = 'DRU', 'Druida del Equilibrio'

    class PhysicalArchetype(models.TextChoices):
        CALISTHENICS = 'CAL', 'Calistenia'
        GYM          = 'GYM', 'Berserker de Gimnasio'
        FLEXIBILITY  = 'FLX', 'Monje de la Flexibilidad'
        RUNNER       = 'RUN', 'Corredor del Viento'

    class SpiritualPath(models.TextChoices):
        ZEN       = 'ZEN', 'Budista Zen'
        CHRISTIAN = 'CHR', 'Cristiano Comprometido'
        STOIC     = 'STO', 'Filósofo Estoico'

    user                  = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name                  = models.CharField(max_length=100)
    level                 = models.IntegerField(default=1)
    xp                    = models.IntegerField(default=0)
    nutritional_archetype = models.CharField(max_length=3, choices=NutritionalArchetype.choices)
    physical_archetype    = models.CharField(max_length=3, choices=PhysicalArchetype.choices)
    spiritual_path        = models.CharField(max_length=3, choices=SpiritualPath.choices)
    login_streak          = models.IntegerField(default=0)
    spiritual_streak      = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Lvl {self.level})"


class Quest(models.Model):
    name        = models.CharField(max_length=200)
    description = models.TextField()
    xp_value    = models.IntegerField(default=10)

    def __str__(self):
        return self.name


class DailyLog(models.Model):
    character       = models.ForeignKey(Character, on_delete=models.CASCADE)
    quest           = models.ForeignKey(Quest, on_delete=models.CASCADE)
    completion_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('character', 'quest', 'completion_date')
