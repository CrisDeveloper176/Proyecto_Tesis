from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Vehiculo
from rest_framework import viewsets
from django.http import JsonResponse


# Create your views here.
@login_required(login_url='/login/')
def home(request):
       return render(request, 'Home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('Home.html')  
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

def vehiculos(request):
     return render(request, "Vehiculos.html")

def monitoring_view(request):
     return render(request, 'monitoring.html')

def Reportes(request):
     return render(request, 'Reportes.html')

def obtener_ubicacion_vehiculo(request):
 
    vehiculo = Vehiculo.objects.last()  
    if vehiculo:
        data = {
            "lat": vehiculo.latitud,
            "lng": vehiculo.longitud
        }
    else:
        data = {"error": "No se encontraron datos de ubicación."}
    return JsonResponse(data)

from django.shortcuts import render
import coreapi

def listar_reportes(request):
    # Inicializar el cliente y cargar el esquema
    client = coreapi.Client()
    schema = client.get("http://api-tesis-muddy-snow-7061.fly.dev/docs/")

    # Definir las acciones para cada endpoint
    endpoints = {
        "viajes": ["Viaje", "list"],
        "vehiculos": ["vehiculo", "list"],
        "mantenimiento": ["Mantenimiento_Vehiculo", "list"],
        "alertas": ["Alertas", "list"]
    }

    # Diccionario para almacenar los resultados de cada endpoint
    data = {}
    for key, action in endpoints.items():
        try:
            data[key] = client.action(schema, action)
        except coreapi.exceptions.ErrorMessage as e:
            data[key] = {"error": f"No se pudo obtener la lista de {key}: {str(e)}"}

    # Pasar los datos a la plantilla
    return render(request, "listar_reportes.html", data)
