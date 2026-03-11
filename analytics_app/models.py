from django.db import models
from django.core.validators import MinValueValidator
from player_app.models import KidProfile


class GameSession(models.Model):
    kid = models.ForeignKey(
        KidProfile,
        on_delete=models.CASCADE,
        related_name='game_sessions'
    )

    task_name = models.CharField(max_length=100)
    score_earned = models.PositiveIntegerField(default=0)

    time_spent = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Time taken to complete the task in seconds."
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Game Session"

    def __str__(self):
        return f"{self.kid.name} - {self.task_name}"

    def get_seconds_per_point(self):
        if self.score_earned > 0:
            return round(self.time_spent / self.score_earned, 2)
        return "N/A"


class BaseQuest(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    participants = models.ManyToManyField(
        KidProfile,
        related_name='active_quests',
        blank=True
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['created_at']

    def __str__(self):
        return self.title


class TrainingQuest(BaseQuest):
    required_completion_count = models.PositiveIntegerField(
        default=5,
        help_text="Tasks needed to finish this training mission."
    )

    completion_bonus = models.PositiveIntegerField(default=50)

    def calculate_bonus(self, total_sessions):
        if total_sessions >= self.required_completion_count:
            return self.completion_bonus
        return 0