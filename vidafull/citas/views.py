from django.shortcuts import render, redirect
from .models import Cita, Especialista, Paciente, Ciudad  
from django.utils import timezone
from datetime import datetime
import json


# Vista para ver historial de citas
def citas(request):
    # Filtra las citas del usuario actual
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha', '-hora')

    return render(request, 'citas/citas.html', {'citas': citas, 'pagina_actual': 'citas'})



# Vista para la página principal (calendario del médico)
def inicio(request):
    # Obtener todas las citas de hoy
    citas = Cita.objects.filter(fecha=timezone.now().date()).order_by('hora')

    # Crear JSON de citas
    citas_json = json.dumps([{
        'title': cita.paciente.nombre,
        'start': cita.fecha_hora().isoformat() if cita.fecha_hora() else None,
        'end': (cita.fecha_hora() + timezone.timedelta(hours=1)).isoformat() if cita.fecha_hora() else None,
        'descripcion': cita.motivo,
    } for cita in citas if cita.fecha_hora() is not None])  # Solo incluye citas válidas

    # Obtener todas las ciudades
    ciudades = Ciudad.objects.all()

    return render(request, 'citas/inicio.html', {
        'citas_json': citas_json,
        'ciudades': ciudades,
        'pagina_actual': 'programar'
    })


# Vista para programar citas
def programar_cita(request):
    # Obtener todas las citas de hoy
    citas = Cita.objects.filter(fecha=timezone.now().date()).order_by('hora')

    # Crear JSON de citas
    citas_json = json.dumps([{
        'title': cita.paciente.nombre,
        'start': cita.fecha_hora().isoformat() if cita.fecha_hora() else None,
        'end': (cita.fecha_hora() + timezone.timedelta(hours=1)).isoformat() if cita.fecha_hora() else None,
        'descripcion': cita.motivo,
    } for cita in citas if cita.fecha_hora() is not None])  # Solo incluye citas válidas

    # Obtener todas las ciudades
    ciudades = Ciudad.objects.all()

    return render(request, 'citas/programar.html', {
        'citas_json': citas_json,
        'ciudades': ciudades,
        'pagina_actual': 'programar'
    })


