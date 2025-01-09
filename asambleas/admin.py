from django.contrib import admin
from .models import Trabajador, Asamblea, Asistencia

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('ficha', 'nombre', 'primer_apellido', 'segundo_apellido', 'centro_trabajo')

@admin.register(Asamblea)
class AsambleaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha', 'link')

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'asamblea', 'confirmacion', 'fecha')
