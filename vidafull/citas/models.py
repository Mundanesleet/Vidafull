from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User

class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Especialista(models.Model):
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    ciudades = models.ManyToManyField(Ciudad, related_name='especialistas')

    def __str__(self):
        return self.nombre

class Disponibilidad(models.Model):
    especialista = models.ForeignKey(Especialista, on_delete=models.CASCADE, related_name='disponibilidades')
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.especialista} disponible en {self.ciudad} el {self.fecha} de {self.hora_inicio} a {self.hora_fin}"

class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=50, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20, blank=True)
    correo = models.EmailField(max_length=100, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=255, blank=True)
    edificio = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre

class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Agregar campo a User
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(null=True, blank=True)
    motivo = models.CharField(max_length=255)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    disponibilidad = models.ForeignKey(Disponibilidad, on_delete=models.CASCADE, null=True, blank=True)
    detalles = models.TextField(blank=True, null=True)

    

    def fecha_hora(self):
        if self.hora is not None:
            return datetime.combine(self.fecha, self.hora)
        return None

    def __str__(self):
        return f"Cita de {self.paciente} con {self.disponibilidad.especialista} el {self.fecha} a las {self.hora}"
