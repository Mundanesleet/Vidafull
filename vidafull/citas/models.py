from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError



class Paciente(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='pacientes_citas')
    nombre = models.CharField(max_length=100, null=True, blank=True)
    apellido = models.CharField(max_length=100, null=True, blank=True)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    edificio = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None

    def __str__(self):
        return f"{self.cedula} - {self.telefono} - {self.correo}"


class Archivo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='archivos_pacientes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)


class Ciudades_disponibles(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Direccion(models.Model):
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return self.direccion


class Disponibilidad(models.Model):
    dia = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)  
    hora_fin = models.TimeField(null=True, blank=True)  
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"Disponibilidad el {self.dia} de {self.hora_inicio} a {self.hora_fin} en {self.ciudad}, {self.direccion}"


class Cita(models.Model):
    from pacientes.models import Paciente
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    hora = models.TimeField(null=True, blank=True)
    disponibilidad = models.ForeignKey(Disponibilidad, null=True, blank=True, on_delete=models.SET_NULL)
    nota = models.TextField(null=True, blank=True)

    def fecha_hora(self):
        if self.hora:
            return timezone.datetime.combine(self.fecha, self.hora)
        return None

    def __str__(self):
        return f"Cita de {self.paciente} el {self.fecha} a las {self.hora}"
    
    # Puedes agregar validación aquí si es necesario para evitar citas duplicadas
    def clean(self):
        # Verifica si la fecha y hora están disponibles en las disponibilidades
        disponibilidad = Disponibilidad.objects.filter(
            dia=self.fecha,
            hora_inicio__lte=self.hora,
            hora_fin__gte=self.hora
        ).exists()

        if not disponibilidad:
            raise ValidationError("El horario no está disponible.")

        # Verifica si ya hay una cita en esa fecha y hora
        cita_existente = Cita.objects.filter(
            fecha=self.fecha,
            hora=self.hora
        ).exists()

        if cita_existente:
            raise ValidationError("Ya hay una cita agendada en este horario.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)