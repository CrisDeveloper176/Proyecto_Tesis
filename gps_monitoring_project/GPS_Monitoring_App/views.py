from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import Vehiculo
from rest_framework import viewsets
from django.http import JsonResponse
from django.shortcuts import render
import coreapi
import requests

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



class APIClient:
    

    def __init__(self, base_url):
        self.base_url = base_url

    def get_data(self, endpoint):
       
        try:
            response = requests.get(endpoint)
            response.raise_for_status()  # Verifica que la respuesta sea exitosa
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"No se pudo obtener la lista de {endpoint}: {str(e)}"}


class ReportService:
    """Clase para gestionar los reportes"""

    def __init__(self, api_client):
        self.api_client = api_client
        # Definir los endpoints específicos para cada recurso
        self.endpoints = {
            "viajes": f"{self.api_client.base_url}Viaje/",
            "vehiculos": f"{self.api_client.base_url}vehiculo/",
            "mantenimiento": f"{self.api_client.base_url}Mantenimiento_Vehiculo/",
            "alertas": f"{self.api_client.base_url}Alertas/"
        }

    def obtener_reportes(self):
        """Obtiene los reportes de todos los endpoints definidos"""
        data = {}
        for key, endpoint in self.endpoints.items():
            data[key] = self.api_client.get_data(endpoint)
        return data


def listar_reportes(request):
    # Inicializar el cliente de API y el servicio de reportes
    api_client = APIClient(base_url="https://apitesis.fly.dev/api/v1/")
    report_service = ReportService(api_client)

    # Obtener los datos de los reportes
    data = report_service.obtener_reportes()

    # Pasar los datos a la plantilla
    return render(request, "listar_reportes.html", data)



def crear_arrendatario(request):
    # Inicializa el cliente de la API
    client = coreapi.Client()
    
    # Obtiene el esquema de la API
    schema = client.get("https://apitesis.fly.dev/api/v1/Arrendatarios/")
    
    # Los parámetros del arrendatario que quieres crear
    params = {
        "Rut": "12345678-9",  # ejemplo, reemplaza con los datos correctos
        "Nombre": "Juan",
        "Apellido": "Pérez",
        "Licencia_Conducir": "1234",
        "Telefono": "123456789",
        "Correo": "juan.perez@example.com",
    }
    
    # Acción para crear el arrendatario
    action = ["Arrendatarios", "create"]
    
    # Llama a la API
    result = client.action(schema, action, params=params)
    
    # Renderiza el resultado en una plantilla o haz lo que necesites
    return render(request, 'arrendatarios.html', {'arrendatarios': result})
