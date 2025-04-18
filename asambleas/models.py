from django.db import models

# Create your models here.

class Trabajador(models.Model):
    ficha = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    regimen_contractual = models.CharField(max_length=50)
    departamento = models.CharField(max_length=100)
    clave_centro_trabajo = models.CharField(max_length=50)
    centro_trabajo = models.CharField(max_length=100)

    def __str__(self):
        return str(self.nombre)
    
class Asamblea(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    link = models.CharField(max_length=200)
    fecha = models.DateTimeField()
    longitud = models.FloatField()
    latitud = models.FloatField()
    def __str__(self):
        return self.nombre
    
class Asistencia(models.Model):
    trabajador = models.ForeignKey(Trabajador, on_delete=models.CASCADE)
    asamblea = models.ForeignKey(Asamblea, on_delete=models.CASCADE)
    confirmacion = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('trabajador', 'asamblea')
        
        def __str__(self):
            return str(self.trabajador, self.asamblea)