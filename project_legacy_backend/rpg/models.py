from django.db import models
# Ahora importamos todo lo necesario desde legacy_core
from legacy_core.models import (
    Player, 
    NutritionalArchetype, 
    PhysicalArchetype, 
    SpiritualPath
)

# --- Sistema de Misiones (Quests) ---

class QuestType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Quest(models.Model):
    """ Plantilla para una misión. """
    name = models.CharField(max_length=200) # Changed from title to name
    description = models.TextField()
    xp_reward = models.PositiveIntegerField(default=10)
    quest_type = models.ForeignKey(QuestType, on_delete=models.SET_NULL, null=True, blank=True) # Added quest_type
    time_of_day = models.CharField(
        max_length=10,
        choices=[
            ('Morning', 'Morning'),
            ('Afternoon', 'Afternoon'),
            ('Night', 'Night'),
        ],
        default='Morning'
    )
    
    # Las relaciones ahora apuntan a los modelos en legacy_core
    nutritional_archetype_quest = models.ForeignKey(
        NutritionalArchetype, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="fundamental_quests"
    )
    physical_archetype_quest = models.ForeignKey(
        PhysicalArchetype, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name="fundamental_quests"
    )
    is_spiritual_quest = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PlayerQuest(models.Model):
    """
    Una instancia de una misión asignada a un jugador en un día concreto.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="quests")
    quest = models.ForeignKey(Quest, on_delete=models.CASCADE)
    date_assigned = models.DateField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('player', 'quest', 'date_assigned')

    def __str__(self):
        return f"{self.player.user.username} - {self.quest.name} ({'Completada' if self.is_completed else 'Pendiente'})"

# --- Sistema de Logros y Recompensas a Largo Plazo ---

class Achievement(models.Model):
    """
    Medallas y reconocimientos a largo plazo.
    """
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class PlayerAchievement(models.Model):
    """
    Vincula un logro a un jugador.
    """
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_unlocked = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('player', 'achievement')

    def __str__(self):
        return f"{self.player.user.username} desbloqueó {self.achievement.name}"