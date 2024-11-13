# admin.py
from django.contrib import admin
from .models import Paciente, Cita, Especialista, Ciudad  # Asegúrate de importar Ciudad

# Registro de modelos existentes
admin.site.register(Paciente)
admin.site.register(Cita)
admin.site.register(Especialista)

# Registro del modelo Ciudad
@admin.register(Ciudad)
class CiudadAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra las columnas que quieres en la lista
