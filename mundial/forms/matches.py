from django import forms
from ..models import Prediction


class PredictionForm(forms.Form):
    CHOICE_CHOICES = Prediction.CHOICE_CHOICES

    choice = forms.ChoiceField(choices=CHOICE_CHOICES, widget=forms.HiddenInput)
