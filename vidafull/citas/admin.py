from django.contrib import admin
from .models import Paciente, Cita, Ciudades_disponibles

# Registro del modelo Paciente con configuración personalizada
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'apellido', 'telefono', 'correo', 'ciudad', 'direccion', 'edificio', 'fecha_nacimiento', 'edad')
    fields = ('user', 'nombre', 'apellido', 'cedula', 'telefono', 'correo', 'ciudad', 'direccion', 'edificio', 'fecha_nacimiento')
    search_fields = ('cedula', 'nombre', 'apellido', 'correo')
    list_filter = ('ciudad',)
    readonly_fields = ('edad',)  # Mostrar la edad como campo de solo lectura

# Registro del modelo Ciudades_disponibles
@admin.register(Ciudades_disponibles)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

# Registro del modelo Cita sin el campo 'especialista'
@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'fecha', 'nota')  
    fields = ('paciente', 'fecha', 'hora','nota')
    search_fields = ('paciente__nombre', 'paciente__apellido')
    list_filter = ('fecha',)  # Sin 'especialista' en el filtro
