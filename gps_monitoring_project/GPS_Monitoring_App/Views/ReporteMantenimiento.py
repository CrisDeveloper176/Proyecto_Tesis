from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import requests

def mantenimientoreport_view(request):
     return render(request, 'Reportes/ReporteMantenimiento.html')
def obtener_mantenimiento(request):
    """
    Función para obtener los datos de mantenimiento desde la API con parámetros opcionales
    y enviarlos a una página ya renderizada.
    """
    URL_API_MANTENIMIENTO = "https://apitesis.fly.dev/api/v1/Mantenimiento_Vehiculo/"

    params = {
        "Fecha_Inicio": request.GET.get('Fecha_Inicio'),
        "Fecha_Fin": request.GET.get('Fecha_Fin'),
        "ID_Vehiculo": request.GET.get('ID_Vehiculo'),
        "ID_Mantenimiento": request.GET.get('ID_Mantenimiento'),
    }


    params = {k: v for k, v in params.items() if v is not None}


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

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'mantenimiento': mantenimiento})

    return JsonResponse({'error': 'Solo solicitudes AJAX permitidas'}, status=400)