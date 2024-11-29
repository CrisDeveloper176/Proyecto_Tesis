from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import json
import requests

def Reporte_Vehiculo(request):
    return render(request,'Reportes/ReporteVehiculo.html')

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
