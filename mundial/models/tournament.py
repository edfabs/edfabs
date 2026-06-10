import uuid
from datetime import timedelta
from django.db import models
from django.utils.timezone import now as tz_now


class Team(models.Model):
    name = models.CharField(max_length=100)
    fifa_code = models.CharField(max_length=3, unique=True)
    group = models.CharField(max_length=1, null=True, blank=True)
    flag_url = models.URLField(blank=True)

    class Meta:
        app_label = 'mundial'
        ordering = ['group', 'name']

    def __str__(self):
        return f'{self.name} ({self.fifa_code})'


class Match(models.Model):
    GROUPS = 'GROUPS'
    ROUND_OF_32 = 'ROUND_OF_32'
    ROUND_OF_16 = 'ROUND_OF_16'
    QUARTERFINAL = 'QUARTERFINAL'
    SEMIFINAL = 'SEMIFINAL'
    THIRD_PLACE = 'THIRD_PLACE'
    FINAL = 'FINAL'

    PHASE_CHOICES = [
        (GROUPS, 'Fase de Grupos'),
        (ROUND_OF_32, 'Ronda de 32'),
        (ROUND_OF_16, 'Octavos de Final'),
        (QUARTERFINAL, 'Cuartos de Final'),
        (SEMIFINAL, 'Semifinal'),
        (THIRD_PLACE, 'Tercer Lugar'),
        (FINAL, 'Final'),
    ]

    SCHEDULED = 'SCHEDULED'
    IN_PLAY = 'IN_PLAY'
    FINISHED = 'FINISHED'
    STATUS_CHOICES = [
        (SCHEDULED, 'Programado'),
        (IN_PLAY, 'En Juego'),
        (FINISHED, 'Finalizado'),
    ]

    HOME = 'HOME'
    DRAW = 'DRAW'
    AWAY = 'AWAY'
    WINNER_CHOICES = [
        (HOME, 'Local'),
        (DRAW, 'Empate'),
        (AWAY, 'Visitante'),
    ]

    PHASE_ORDER = [GROUPS, ROUND_OF_32, ROUND_OF_16, QUARTERFINAL, SEMIFINAL, THIRD_PLACE, FINAL]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='home_matches'
    )
    away_team = models.ForeignKey(
        Team, null=True, blank=True, on_delete=models.SET_NULL, related_name='away_matches'
    )
    phase = models.CharField(max_length=20, choices=PHASE_CHOICES)
    group = models.CharField(max_length=1, null=True, blank=True)
    match_date = models.DateTimeField()
    stadium = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=SCHEDULED)
    home_goals = models.IntegerField(null=True, blank=True)
    away_goals = models.IntegerField(null=True, blank=True)
    winner = models.CharField(max_length=10, choices=WINNER_CHOICES, null=True, blank=True)
    match_number = models.PositiveIntegerField(default=0)

    class Meta:
        app_label = 'mundial'
        ordering = ['match_date', 'match_number']

    def __str__(self):
        home = self.home_team.name if self.home_team else 'TBD'
        away = self.away_team.name if self.away_team else 'TBD'
        return f'{home} vs {away} — {self.get_phase_display()}'

    @property
    def prediction_deadline(self):
        return self.match_date - timedelta(hours=1)

    @property
    def is_open_for_predictions(self):
        return tz_now() < self.prediction_deadline

    @property
    def home_display(self):
        return self.home_team.name if self.home_team else 'Por definir'

    @property
    def away_display(self):
        return self.away_team.name if self.away_team else 'Por definir'


class PointConfig(models.Model):
    phase = models.CharField(max_length=20, choices=Match.PHASE_CHOICES, unique=True)
    points = models.IntegerField(default=1)

    class Meta:
        app_label = 'mundial'

    def __str__(self):
        return f'{self.get_phase_display()}: {self.points} pts'
