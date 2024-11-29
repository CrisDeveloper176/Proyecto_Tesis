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

    return render(request, 'Reportes/ReporteViaje.html', {'arrendatarios': arrendatarios})





