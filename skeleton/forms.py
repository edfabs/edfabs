from cProfile import label
from django import forms

class Contacto(forms.Form):
    name = forms.CharField(label='Nombre', max_length=200)
    sender = forms.EmailField(label='E-mail', max_length=150)
    mensaje = forms.CharField(label='Mensjale',widget=forms.Textarea)