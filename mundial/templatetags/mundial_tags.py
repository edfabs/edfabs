from django import template

register = template.Library()


@register.filter
def dict_get(d, key):
    """Accede a un diccionario con clave dinámica (convierte UUID/int a str): {{ my_dict|dict_get:key }}"""
    if d is None:
        return None
    result = d.get(str(key))
    if result is None:
        result = d.get(key)
    return result


@register.filter
def choice_label(choice_value):
    """Retorna el label legible de una elección de predicción."""
    labels = {
        'HOME_WIN': 'Local',
        'DRAW': 'Empate',
        'AWAY_WIN': 'Visitante',
    }
    return labels.get(choice_value, choice_value)
