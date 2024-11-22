from django.db import models
from django.utils import timezone
from datetime import date
from django.contrib.auth.models import User


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
    nota = models.TextField(null=True, blank=True)
    
    @property
    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            # Calcula la edad en función de la fecha de nacimiento
            return today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return None  # Si no hay fecha de nacimiento, retorna None

    def __str__(self):
        return f"{self.cedula} - {self.telefono} - {self.correo}"

    
   

class Archivo(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='archivos')
    archivo = models.FileField(upload_to='archivos_pacientes/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    
    # Puedes agregar más campos, como un título o descripción



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
    dia = models.DateField()
    hora_inicio = models.DateTimeField(null=True, blank=True)  # Permite valores nulos
    hora_fin = models.DateTimeField(null=True, blank=True)  # Permite valores nulos
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)

    def __str__(self):
        return f"Disponibilidad el {self.dia} de {self.hora_inicio} a {self.hora_fin} en {self.ciudad}, {self.direccion}"
    
    

class Cita(models.Model):
    from pacientes.models import Paciente
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)  # Fecha específica de la cita
    hora = models.TimeField(null=True, blank=True)  # Hora específica de la cita
    disponibilidad = models.ForeignKey(Disponibilidad, null=True, blank=True, on_delete=models.SET_NULL)  # Referencia a disponibilidad
    nota = models.TextField(null=True, blank=True)  # Campo para la nota del paciente, opcional
    
    def fecha_hora(self):
        if self.hora:
            return timezone.datetime.combine(self.fecha, self.hora)
        return None

    def __str__(self):
        # Verifica si disponibilidad no es None antes de acceder a sus atributos
        if self.disponibilidad:
            return f"Cita de {self.paciente} el {self.fecha} a las {self.hora} en {self.disponibilidad.ciudad}, {self.disponibilidad.direccion}"
        else:
            return f"Cita de {self.paciente} el {self.fecha} a las {self.hora}"