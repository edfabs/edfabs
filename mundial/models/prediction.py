import uuid
from django.db import models
from django.conf import settings


class Prediction(models.Model):
    HOME_WIN = 'HOME_WIN'
    DRAW = 'DRAW'
    AWAY_WIN = 'AWAY_WIN'
    CHOICE_CHOICES = [
        (HOME_WIN, 'Victoria Local'),
        (DRAW, 'Empate'),
        (AWAY_WIN, 'Victoria Visitante'),
    ]

    PENDING = 'PENDING'
    CORRECT = 'CORRECT'
    INCORRECT = 'INCORRECT'
    NULL = 'NULL'
    RESULT_CHOICES = [
        (PENDING, 'Pendiente'),
        (CORRECT, 'Correcta'),
        (INCORRECT, 'Incorrecta'),
        (NULL, 'Nula'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='predictions'
    )
    match = models.ForeignKey(
        'mundial.Match', on_delete=models.CASCADE, related_name='predictions'
    )
    choice = models.CharField(max_length=10, choices=CHOICE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_locked = models.BooleanField(default=False)
    result = models.CharField(max_length=10, choices=RESULT_CHOICES, default=PENDING)

    class Meta:
        app_label = 'mundial'
        unique_together = [('user', 'match')]

    def __str__(self):
        return f'{self.user.email} — {self.match} — {self.get_choice_display()}'


class UserScore(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mundial_score'
    )
    total_points = models.IntegerField(default=0)
    correct_predictions = models.IntegerField(default=0)
    incorrect_predictions = models.IntegerField(default=0)
    null_predictions = models.IntegerField(default=0)
    playoff_correct = models.IntegerField(default=0)

    class Meta:
        app_label = 'mundial'

    def __str__(self):
        return f'{self.user.email}: {self.total_points} pts'
