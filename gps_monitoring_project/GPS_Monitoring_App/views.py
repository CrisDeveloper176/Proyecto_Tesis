from django.contrib.auth.decorators import login_required
from .models import Vehiculo
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests
import coreapi


# Create your views here.
@login_required(login_url='/login/')
def home(request):
       return render(request, 'Home.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica si los datos están vacíos
        if not username or not password:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # URL del endpoint de la API
        url = "http://apitesis.fly.dev/api/v1/token/"  # Cambia la URL si es necesario

        # Parámetros para la solicitud
        data = {
            "username": username,
            "password": password,
        }
        headers = {
            "Content-Type": "application/json",
        }

        try:
            # Realiza la solicitud POST
            response = requests.post(url, data=json.dumps(data), headers=headers)
            if response.status_code == 200:
                # Guarda el token en la sesión
                tokens = response.json()
                access_token = tokens.get('access')
                refresh_token = tokens.get('refresh')

                if not access_token or not refresh_token:
                    return JsonResponse({'error': 'No se recibieron tokens de acceso.'}, status=500)

                request.session['access_token'] = access_token
                request.session['refresh_token'] = refresh_token

                return redirect('home')  # Redirige a la página de inicio
            else:
                error_message = response.json().get('detail', 'Credenciales inválidas o error desconocido.')
                return JsonResponse({'error': error_message}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Error al autenticar el usuario: {e}")
            return JsonResponse({'error': 'Error de conexión con la API.'}, status=500)

    return render(request, 'login.html')



def monitoring_view(request):
     return render(request, 'monitoring.html')

def Reportes(request):
     return render(request, 'Reportes.html')
 
def Arrendatarios(request):
    return render(request= 'arrendatarios.html')

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

def getAPI(request):
     URL_API = "https://apitesis.fly.dev/api/v1/vehiculo/"
     
     response = requests.get(URL_API)
     if response.status_code == 200:
        vehiculo = response.json()
         
        for producto in vehiculo:
            print(producto)
            
        return HttpResponse(vehiculo) or []
         

def obtener_vehiculo(request):
    
    URL_API = "https://apitesis.fly.dev/api/v1/vehiculo/"
    try:
        
        response = requests.get(URL_API)
        if response.status_code == 200:
            vehiculos = response.json()
        else:
            print(f"Error en la solicitud: {response.status_code}")
            vehiculos = []
    except requests.RequestException as e:
        print(f"Error en la solicitud: {e}")
        vehiculos = []
    
    return render(request, 'vehiculos.html',{'vehiculos': vehiculos})







