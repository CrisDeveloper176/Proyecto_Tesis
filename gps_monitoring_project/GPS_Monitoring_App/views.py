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
