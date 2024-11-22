from django.contrib.auth.models import User
from django.db import models




# Create your models here.

class Paciente(models.Model):
    from citas.models import Ciudades_disponibles
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes')
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=100, blank=True)
    ciudad = models.ForeignKey(Ciudades_disponibles, on_delete=models.SET_NULL, null=True, blank=True)  # Cambio aquí
    direccion = models.CharField(max_length=255, blank=True)
    edificio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre