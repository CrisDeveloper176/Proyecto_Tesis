from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests

def obtener_viajes(request):
    """
    Función para renderizar la página de viajes con los datos obtenidos de la API.
    """
    URL_API_VIAJES = "https://apitesis.fly.dev/api/v1/Viaje/"

    # Obtener viajes
    try:
        response_viajes = requests.get(URL_API_VIAJES)
        if response_viajes.status_code == 200:
            arrendatarios = response_viajes.json()
        else:
            arrendatarios = []
            print("Error al obtener viajes")
    except requests.RequestException as e:
        print(f"Error al obtener viajes: {e}")
        arrendatarios = []

    return render(request, 'Reportes/Reportes.html', {'arrendatarios': arrendatarios})



def obtener_modelos_y_vehiculos_reporte(request):
    """
    Función para obtener los datos de vehículos y modelos desde la API y enviarlos a una página ya renderizada.
    """
    URL_API_MODELOS = "https://apitesis.fly.dev/api/v1/Modelo/"
    URL_API_VEHICULOS = "https://apitesis.fly.dev/api/v1/vehiculo/"

    # Obtener modelos
    try:
        response_modelos = requests.get(URL_API_MODELOS)
        if response_modelos.status_code == 200:
            modelos = response_modelos.json()
        else:
            modelos = []
            print("Error al obtener modelos")
    except requests.RequestException as e:
        print(f"Error al obtener modelos: {e}")
        modelos = []

    # Obtener vehículos
    try:
        response_vehiculos = requests.get(URL_API_VEHICULOS)
        if response_vehiculos.status_code == 200:
            vehiculos = response_vehiculos.json()
        else:
            vehiculos = []
    except requests.RequestException as e:
        print(f"Error al obtener vehículos: {e}")
        vehiculos = []

    # Asociar el nombre del modelo a cada vehículo
    for vehiculo in vehiculos:
        vehiculo['modelo_nombre'] = next(
            (modelo['Nombre_Modelo'] for modelo in modelos if modelo['ID_Modelo'] == vehiculo['ID_Modelo']), 
            None
        )

    # Verificar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'vehiculos': vehiculos, 'modelos': modelos})

    # Si no es AJAX, no responde. Podrías manejar errores o mensajes aquí.
    return JsonResponse({'error': 'Solo solicitudes AJAX permitidas'}, status=400)

from django.http import JsonResponse
import requests

def obtener_mantenimiento(request):
    """
    Función para obtener los datos de mantenimiento desde la API con parámetros opcionales
    y enviarlos a una página ya renderizada.
    """
    URL_API_MANTENIMIENTO = "https://apitesis.fly.dev/api/v1/Mantenimiento_Vehiculo/"

    # Obtener parámetros de la solicitud
    params = {
        "Fecha_Inicio": request.GET.get('Fecha_Inicio'),
        "Fecha_Fin": request.GET.get('Fecha_Fin'),
        "ID_Vehiculo": request.GET.get('ID_Vehiculo'),
        "ID_Mantenimiento": request.GET.get('ID_Mantenimiento'),
    }

    # Limpiar los parámetros para evitar enviar None si no están presentes
    params = {k: v for k, v in params.items() if v is not None}

    # Obtener mantenimiento
    try:
        response_mantenimiento = requests.get(URL_API_MANTENIMIENTO, params=params)
        if response_mantenimiento.status_code == 200:
            mantenimiento = response_mantenimiento.json()
        else:
            mantenimiento = []
            print("Error al obtener mantenimiento")
    except requests.RequestException as e:
        print(f"Error al obtener mantenimiento: {e}")
        mantenimiento = []

    # Verificar si la solicitud es AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'mantenimiento': mantenimiento})

    # Si no es AJAX, manejar errores
    return JsonResponse({'error': 'Solo solicitudes AJAX permitidas'}, status=400)

