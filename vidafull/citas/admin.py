# admin.py
from django.contrib import admin

from pacientes.models import Paciente
from .models import Cita, Especialista, Ciudades_disponibles  # Asegúrate de importar Ciudad

# Registro de modelos existentes
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Especialista)

# Registro del modelo Ciudad
@admin.register(Ciudades_disponibles)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra las columnas que quieres en la lista
