from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User



class Ciudades_disponibles(models.Model):
    nombre = models.CharField(max_length=100)

    # class Meta:
    #     db_table = 'citas_ciudad'

    def __str__(self):
        return self.nombre

class Direccion(models.Model):
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.direccion

class Especialista(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    ciudades = models.ManyToManyField(Ciudades_disponibles, related_name='especialistas')

    def __str__(self):
        return self.nombre
    
class Disponibilidad(models.Model):
    dia = models.DateField()  # Día específico de disponibilidad
    hora_inicio = models.TimeField()  # Hora de inicio de disponibilidad
    hora_fin = models.TimeField()  # Hora de fin de disponibilidad
    ciudad = models.CharField(max_length=100)  # Ciudad donde estará disponible
    direccion = models.CharField(max_length=255)  # Dirección exacta

    def __str__(self):
        return f"Disponibilidad el {self.dia} de {self.hora_inicio} a {self.hora_fin} en {self.ciudad}, {self.direccion}"
    
    

class Cita(models.Model):
    from pacientes.models import Paciente
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)  # Fecha específica de la cita
    hora = models.TimeField(null=True, blank=True)  # Hora específica de la cita
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.CASCADE)  # Referencia a disponibilidad
    

    def fecha_hora(self):
        if self.hora:
            return timezone.datetime.combine(self.fecha, self.hora)
        return None

    def __str__(self):
        return f"Cita de {self.paciente} el {self.fecha} a las {self.hora} en {self.disponibilidad.ciudad}, {self.disponibilidad.direccion}"