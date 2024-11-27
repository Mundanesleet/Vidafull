from django.shortcuts import render, redirect
from .models import Cita, Ciudades_disponibles, Disponibilidad, Direccion
from django.utils import timezone
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.http import HttpResponseBadRequest
from .serializers import DireccionSerializer
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
import locale
from .models import Paciente, Archivo
from datetime import timedelta, datetime, date


#Clases creadas
class create_address(generics.CreateAPIView):
    queryset = Direccion.objects.all()
    serializer_class = DireccionSerializer

#Citas programadas
def citas(request):
    # Configura el idioma en español (esto funciona en sistemas compatibles)
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  # En Windows, usa 'Spanish_Spain.1252'

    # Obtener la fecha actual como objeto datetime.date
    fecha_actual = timezone.now().date()

    # Si el usuario quiere ver citas de otro día
    if 'fecha' in request.GET:
        fecha_str = request.GET['fecha']
        fecha_actual = datetime.strptime(fecha_str, "%Y-%m-%d").date()

    # Consultar citas del día
    citas_del_dia = Cita.objects.filter(fecha=fecha_actual).order_by('hora')

    # Obtener el mes para mostrar
    # Obtener el nombre del día y el mes en español
    dia = fecha_actual.strftime("%A")# Día de la semana en español
    mes = fecha_actual.strftime("%B").capitalize()  # Mes en español
 
    dia = dia.capitalize()
    

    context = {
        'fecha_actual': fecha_actual,
        'citas_del_dia': citas_del_dia,
        'dia': dia,
        'mes': mes,
        'pagina_actual': 'citas',
        'search_type': 'paciente',
    }

    return render(request, 'citas.html', context)



@csrf_exempt
def cargar_archivos(request, paciente_id):
    paciente = get_object_or_404(Paciente, pk=paciente_id)

    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        
        # Guardar el archivo en el modelo Archivo
        nuevo_archivo = Archivo(paciente=paciente, archivo=archivo)
        nuevo_archivo.save()
        
        return JsonResponse({'success': True, 'message': 'Archivo cargado correctamente'})
    
    return JsonResponse({'success': False, 'message': 'No se recibió un archivo válido'}, status=400)


#Programar citas
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
        horas_disponibles = [hora for hora in range(7, 20) if hora not in horas_ocupadas and hora not in horas_seleccionadas]

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
            'pagina_actual': 'programar',
            'search_type': 'fecha',
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
            'pagina_actual': 'programar',
            'search_type': 'fecha',
        })


def obtener_horas_disponibles(request):
    fecha_seleccionada = request.GET.get("fecha")
    if fecha_seleccionada:
        # Obtener las horas ocupadas para la fecha seleccionada
        citas_ocupadas = Cita.objects.filter(fecha=fecha_seleccionada).values_list("hora", flat=True)
        horas_ocupadas = list(citas_ocupadas)  # Convertir a lista para JSON

        # Opcional: Lista de todas las horas (ajústalo según tu rango de horas)
        todas_las_horas = [f"{hora}:00" for hora in range(7, 20)]  
        horas_disponibles = [hora for hora in todas_las_horas if hora not in horas_ocupadas]

        return JsonResponse({"horas_ocupadas": horas_ocupadas, "horas_disponibles": horas_disponibles})
    return JsonResponse({"error": "Fecha no proporcionada"}, status=400)


#Pacientes
def lista_pacientes(request):
    pacientes = Paciente.objects.all()

    context = {
        'search_type': 'paciente',
        'pacientes': pacientes, 
        'pagina_actual': 'pacientes', # Aquí es para buscar pacientes
    }

    return render(request, 'pacientes.html', context)

#Solicitud para busqueda
def buscar_pacientes(request):
    if request.is_ajax():  # Verifica que sea una solicitud AJAX
        query = request.GET.get('q', '').strip()  # Obtén la consulta del cliente
        pacientes = Paciente.objects.filter(
            nombre__icontains=query
        ) | Paciente.objects.filter(
            apellido__icontains=query
        )

        # Preparar los resultados en formato JSON
        resultados = [
            {'id': p.id, 'nombre': p.nombre, 'apellido': p.apellido, 'telefono': p.telefono} for p in pacientes
        ]

        return JsonResponse({'pacientes': resultados}, safe=False)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def detalles_paciente(request, paciente_id):
    # Obtener al paciente por su id
    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Obtener los exámenes médicos relacionados con el paciente
    examenes = Archivo.objects.filter(paciente=paciente)

    # Pasar los datos al template
    return render(request, 'detalles_paciente.html', {
        'paciente': paciente,
        'examenes': examenes,
        'pagina_actual': 'pacientes',

    })

# Vista para la página principal (calendario del médico)
def inicio(request):
    return render(request, 'inicio_menu.html')




#Agendar citas

def obtener_horarios_disponibles(fecha):
    # Obtiene las disponibilidades para la fecha (sin necesidad de filtrar por medico)
    disponibilidades = Disponibilidad.objects.filter(dia=fecha)

    horarios_disponibles = []
    for disponibilidad in disponibilidades:
        hora_actual = disponibilidad.hora_inicio

        while hora_actual < disponibilidad.hora_fin:
            # Verifica si el horario está ocupado
            cita_ocupada = Cita.objects.filter(
                fecha=fecha,
                hora=hora_actual
            ).exists()

            if not cita_ocupada:
                horarios_disponibles.append(hora_actual)

            # Incrementa la hora por intervalos (e.g., 30 minutos)
            hora_actual = (datetime.combine(date.today(), hora_actual) + timedelta(minutes=30)).time()

    return horarios_disponibles

def agendar_cita(request):
    fecha = request.GET.get('fecha', date.today())
    horarios_disponibles = obtener_horarios_disponibles(fecha)

    if request.method == "POST":
        # Crear el paciente
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        correo = request.POST.get('correo')
        ciudad = request.POST.get('ciudad')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        paciente = Paciente.objects.create(
            nombre=nombre,
            apellido=apellido,
            telefono=telefono,
            correo=correo,
            ciudad=ciudad,
            direccion=direccion,
            fecha_nacimiento=fecha_nacimiento
        )

        # Obtener el horario seleccionado
        horario = request.POST.get('horario')

        if not horario:
            return HttpResponseBadRequest("Debes seleccionar un horario.")

        # Crear la cita para el paciente
        cita = Cita.objects.create(
            paciente=paciente,
            fecha=fecha,
            hora=horario
        )

        # Redirigir a una página de confirmación
        return redirect('confirmacion_cita')

    return render(request, 'agendar_cita.html', {
        'fecha': fecha,
        'horarios_disponibles': horarios_disponibles,
    })