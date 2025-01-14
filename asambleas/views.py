from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Trabajador, Asamblea, Asistencia
import csv
import io
from django.http import HttpResponse
from .forms import UploadFileForm

def index(request):
	#return HttpResponse("Hello, world. You're at te skeleton index")
	return render(request, 'asambleas/index.html', {'title': 'Home'})

def registrar_asistencia(request, asamblea_id):
    asamblea = Asamblea.objects.get(id=asamblea_id)
    trabajadores = Trabajador.objects.all()
    if request.method == 'POST':
        trabajador_id = request.POST.get('trabajador_id')
        trabajador = Trabajador.objects.get(ficha=trabajador_id)

        # Validar geolocalización
        longitud_actual = request.POST.get('longitud')
        latitud_actual = request.POST.get('latitud')
        if longitud_actual == "" or latitud_actual == "":
            messages.error(request, 'Error al registrar asistencia, debes de permitir la geolocalización')
        else:
            if (asamblea.longitud - 0.00225 <= float(longitud_actual) <= asamblea.longitud + 0.00225 and
                asamblea.latitud - 0.00225<= float(latitud_actual) <= asamblea.latitud + 0.00225):
                # Verificar si el trabajador ya se ha registrado
                if (Asistencia.objects.filter(trabajador=trabajador, asamblea=asamblea).exists()):
                    messages.error(request, 'Ya has registrado tu asistencia a esta asamblea.')
                else:
                    # Verificar si ya existe una cookie para este trabajador
                    cookie_name = f'assistencia_{asamblea.id}'
                    if request.COOKIES.get(cookie_name):
                        messages.error(request, 'Ya has registrado tu asistencia a esta asamblea desde este dispositivo.')
                    else:                
                        # Registrar asistencia
                        Asistencia.objects.create(trabajador=trabajador, asamblea=asamblea, confirmacion=True)
                        messages.success(request, 'Asistencia registrada con éxito.')
                        # Establecer la cookie para indicar que el trabajador ha registrado asistencia
                        response = redirect(f'/asambleas/asamblea/{asamblea_id}/registrar/')
                        response.set_cookie(cookie_name, 'true', max_age=60*60*24*30)  # Cookie válida por 30 días
                        
                        return response
            else:
                messages.error(request, 'No se puede registrar la asistencia. Debe estar en el recinto.')

    return render(request, 'asambleas/registrar_asistencia.html', {
        'asamblea': asamblea,
        'trabajadores': trabajadores
        })

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            # Procesar el archivo CSV
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            next(io_string)  # Saltar la cabecera del CSV
            for line in io_string:
                fields = line.strip().split(',')
                # Asegúrate de que el número de campos coincida con tu modelo
                if len(fields) == 6:  # Verifica que haya 6 campos
                    try:
                        trabajador = Trabajador(
                            ficha=fields[0],
                            nombre=fields[1],
                            regimen_contractual=fields[2],
                            departamento=fields[3],
                            clave_centro_trabajo=fields[4],
                            centro_trabajo=fields[5],
                        )
                        trabajador.save()
                    except Exception as e:
                        return HttpResponse(f"Error al guardar el trabajador: {e}")
                else:
                    return HttpResponse("Error: El número de campos en la línea no coincide con el modelo.")
            return HttpResponse("Archivo procesado correctamente.")
    else:
        form = UploadFileForm()
    return render(request, 'asambleas/upload.html', {'form': form})

def reporte_asistencia(request, asamblea_id):
    asamblea = Asamblea.objects.get(id=asamblea_id)
    asistencias = Asistencia.objects.filter(asamblea=asamblea).order_by('-fecha')[:500]
    trabajadores_asistieron = [asistencia.trabajador for asistencia in asistencias if asistencia.confirmacion]
    num_trabajadores = Asistencia.objects.filter(asamblea=asamblea)

    return render(request, 'asambleas/reporte_asistencia.html', {
        'asamblea': asamblea,
        'trabajadores_asistieron': trabajadores_asistieron,
        'num_trabajadores': num_trabajadores
    })
