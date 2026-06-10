from django import forms
from ..models import Match, PointConfig

_FC = lambda extra=None: {'class': 'form-control', **(extra or {})}


class MatchResultForm(forms.Form):
    home_goals = forms.IntegerField(
        min_value=0, max_value=30,
        label='Goles Local',
        widget=forms.NumberInput(attrs=_FC()),
    )
    away_goals = forms.IntegerField(
        min_value=0, max_value=30,
        label='Goles Visitante',
        widget=forms.NumberInput(attrs=_FC()),
    )


class MatchEditForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['home_team', 'away_team', 'match_date', 'stadium', 'city', 'status']
        widgets = {
            'home_team': forms.Select(attrs=_FC()),
            'away_team': forms.Select(attrs=_FC()),
            'match_date': forms.DateTimeInput(
                attrs=_FC({'type': 'datetime-local'}), format='%Y-%m-%dT%H:%M'
            ),
            'stadium': forms.TextInput(attrs=_FC()),
            'city': forms.TextInput(attrs=_FC()),
            'status': forms.Select(attrs=_FC()),
        }
        labels = {
            'home_team': 'Equipo Local',
            'away_team': 'Equipo Visitante',
            'match_date': 'Fecha y Hora',
            'stadium': 'Estadio',
            'city': 'Ciudad',
            'status': 'Estado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Format datetime for the input widget
        if self.instance and self.instance.match_date:
            self.fields['match_date'].initial = (
                self.instance.match_date.strftime('%Y-%m-%dT%H:%M')
            )
