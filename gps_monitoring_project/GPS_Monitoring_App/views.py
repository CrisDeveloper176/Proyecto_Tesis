from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Vehiculo
from django.http import JsonResponse
from django.shortcuts import render,redirect
import coreapi
import json
import requests


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

        # Configura la URL del endpoint de la API
        url = "http://apitesis.fly.dev//api/v1/api/token/"  # Cambia la URL si es necesario

        # Define los parámetros en formato JSON
        data = {
            "username": username,
            "password": password,
        }

        # Configura las cabeceras para enviar JSON
        headers = {
            "Content-Type": "application/json",
        }

        try:
            # Realiza la solicitud POST con los datos en formato JSON
            response = requests.post(url, data=json.dumps(data), headers=headers)

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Guarda el token en la sesión
                token = response.json().get('token')
                request.session['token'] = token
                return redirect('home')  # Redirige a la página de inicio
            else:
                # Si ocurre un error en la API, muestra el mensaje de error
                return JsonResponse({'error': response.text}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            # Maneja los errores de conexión o problemas con la solicitud
            print(f"Error al autenticar el usuario: {e}")
            return JsonResponse({'error': f"Error al autenticar el usuario: {str(e)}"}, status=400)

    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Verifica si los datos están vacíos
        if not username or not email or not password:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # Configura la URL del endpoint de la API
        url = "http://apitesis.fly.dev/api/v1/Login/"  # Cambia la URL si es necesario

        # Define los parámetros en formato JSON
        data = {
            "user": username,  # Reemplaza con 'username' si ese es el parámetro correcto
            "email": email,
            "password": password,
        }

        # Configura las cabeceras para enviar JSON
        headers = {
            "Content-Type": "application/json",
        }

        try:
            # Realiza la solicitud POST con los datos en formato JSON
            response = requests.post(url, data=json.dumps(data), headers=headers)

            # Verifica si la solicitud fue exitosa
            if response.status_code == 200:
                # Redirige a la página de login si el registro fue exitoso
                return redirect('login')
            else:
                # Si ocurre un error en la API, muestra el mensaje de error
                return JsonResponse({'error': response.text}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            # Maneja los errores de conexión o problemas con la solicitud
            print(f"Error al registrar el usuario: {e}")
            return JsonResponse({'error': f"Error al registrar el usuario: {str(e)}"}, status=400)
        
    return render(request, 'register.html')
def vehiculos(request):
     return render(request, "vehiculos.html")

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

def vehiculo_view(request):
    client = coreapi.Client()
    try:
        
        schema = client.get("http://apitesis.fly.dev/docs/")
        
       
        action = ["Modelo", "list"]
        modelos = client.action(schema, action) 

    except coreapi.exceptions.Error as e:
        print(f"Error al cargar modelos desde la API: {e}")
        modelos = [] 

   
    return render(request, 'vehiculos.html', {'modelos': modelos})








