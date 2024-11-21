from django.shortcuts import render, redirect
from .models import Cita, Especialista, Ciudades_disponibles, Disponibilidad, Direccion
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from .serializers import DireccionSerializer
from rest_framework import generics


def obtener_horas_disponibles(request):
    fecha_seleccionada = request.GET.get("fecha")
    if fecha_seleccionada:
        # Obtener las horas ocupadas para la fecha seleccionada
        citas_ocupadas = Cita.objects.filter(fecha=fecha_seleccionada).values_list("hora", flat=True)
        horas_ocupadas = list(citas_ocupadas)  # Convertir a lista para JSON

        # Opcional: Lista de todas las horas (ajústalo según tu rango de horas)
        todas_las_horas = [f"{hora}:00" for hora in range(8, 18)]  # Ejemplo de 8 am a 5 pm
        horas_disponibles = [hora for hora in todas_las_horas if hora not in horas_ocupadas]

        return JsonResponse({"horas_ocupadas": horas_ocupadas, "horas_disponibles": horas_disponibles})
    return JsonResponse({"error": "Fecha no proporcionada"}, status=400)


# Vista para ver historial de citas
def citas(request):
    # Filtra las citas del usuario actual
    citas = Cita.objects.filter(usuario=request.user).order_by('-fecha', '-hora')

    return render(request, 'citas.html', {'citas': citas, 'pagina_actual': 'citas'})


# Vista para la página principal (calendario del médico)
def inicio(request):
    return render(request, 'inicio_menu.html')


class create_address(generics.CreateAPIView):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

# Vista para programar citas
def programar_cita(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        fecha = request.POST.get('fecha')  # Fecha seleccionada
        ciudad_id = request.POST.get('ciudad')  # Ciudad seleccionada
        lugar = request.POST.get('lugar')  # Lugar seleccionado
        horas_seleccionadas = request.POST.getlist('horas')  # Horas seleccionadas (lista)

        # Verificar que la ciudad exista
        ciudad = Ciudades_disponibles.objects.filter(id=ciudad_id).first()
        if not ciudad:
            messages.error(request, "Ciudad no válida.")
            return redirect('programar_cita')

        # Convertir la fecha a un objeto datetime (si es necesario)
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()  # Asume que la fecha es del tipo 'YYYY-MM-DD'
        except ValueError:
            messages.error(request, "La fecha no tiene el formato correcto.")
            return redirect('programar_cita')

        # Validar horas seleccionadas
        horas_seleccionadas = [int(hora) for hora in horas_seleccionadas if hora.isdigit()]

        # Buscar las citas ya programadas para la fecha seleccionada y la ciudad
        citas = Cita.objects.filter(fecha=fecha, disponibilidad__ciudad_id=ciudad_id)
        horas_ocupadas = [cita.hora.hour for cita in citas if cita.hora]

        # Obtener las horas disponibles (por ejemplo, de 7 AM a 6 PM)
        horas_disponibles = [hora for hora in range(7, 19) if hora not in horas_ocupadas and hora not in horas_seleccionadas]

        # Guardar la disponibilidad en la base de datos
        try:
            disponibilidad = Disponibilidad(fecha=fecha, horas_disponibles=horas_disponibles, ciudad_id=ciudad_id, lugar=lugar)
            disponibilidad.save()
            messages.success(request, "¡Disponibilidad registrada con éxito!")
        except Exception as e:
            messages.error(request, f"Ocurrió un error al guardar la disponibilidad: {str(e)}")
            return redirect('programar_cita')

        # Renderizar de nuevo el formulario con las ciudades y horas disponibles
        ciudades = Ciudades_disponibles.objects.all()
        direcciones = Direccion.objects.all()
        return render(request, 'programar.html', {
            'ciudades': ciudades,
            'direcciones': direcciones,
            'horas_disponibles': [str(hora) for hora in range(7, 19)], # Horas de 7 AM a 6 PM
            'horas_ocupadas': horas_ocupadas,
            'pagina_actual': 'programar'
        })

    else:
        # Si es GET, renderizar formulario vacío
        ciudades = Ciudades_disponibles.objects.all()
        direcciones = Direccion.objects.all()
        horas_disponibles = [str(hora) for hora in range(7, 19)]
        horas_ocupadas = []  # Aquí puedes agregar lógica para mostrar citas ocupadas por defecto, si necesario.
        return render(request, 'programar.html', {
            'ciudades': ciudades,
            'direcciones': direcciones,
            'horas_disponibles': horas_disponibles,
            'horas_ocupadas': horas_ocupadas,
            'pagina_actual': 'programar'
        })
