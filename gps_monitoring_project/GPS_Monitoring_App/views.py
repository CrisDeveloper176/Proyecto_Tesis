from django.contrib.auth.decorators import login_required
from .models import Vehiculo
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests
import coreapi


# Create your views here.
@login_required(login_url='TemplatesBase/login/')
def home(request):
       return render(request, 'TemplatesBase/Home.html')

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

                return redirect('TemplatesBase/Home.html')  # Redirige a la página de inicio
            else:
                error_message = response.json().get('detail', 'Credenciales inválidas o error desconocido.')
                return JsonResponse({'error': error_message}, status=response.status_code)

        except requests.exceptions.RequestException as e:
            print(f"Error al autenticar el usuario: {e}")
            return JsonResponse({'error': 'Error de conexión con la API.'}, status=500)

    return render(request, 'TemplatesBase/login.html')



def monitoring_view(request):
     return render(request, 'Monitoreo/monitoring.html')

def Reportes(request):
     return render(request, 'Reportes/Reportes.html')
 
def Arrendatarios(request):
    return render(request, 'CRUD/arrendatarios.html')

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
    # URLs de las APIs
    URL_API_VEHICULOS = "https://apitesis.fly.dev/api/v1/vehiculo/"
    URL_API_MODELOS = "https://apitesis.fly.dev/api/v1/modelo/"

    # Inicializar contenedores para datos
    vehiculos = []
    modelos = []

    # Realizar las solicitudes
    response_vehiculos = requests.get(URL_API_VEHICULOS)
    response_modelos = requests.get(URL_API_MODELOS)

    # Verificar el estado de las respuestas
    if response_vehiculos.status_code == 200:
        vehiculos = response_vehiculos.json()

    if response_modelos.status_code == 200:
        modelos = response_modelos.json()

    # Combinar los datos en un diccionario
    data = {
        "vehiculos": vehiculos,
        "modelos": modelos,
    }

    # Opcional: imprimir los datos para depuración
    for vehiculo in vehiculos:
        print(vehiculo)

    for modelo in modelos:
        print(modelo)

    # Convertir el diccionario a una cadena JSON
    response_data = json.dumps(data, ensure_ascii=False, indent=4)

    # Retornar como HttpResponse
    return HttpResponse(response_data, content_type="application/json")
         

def obtener_modelos_y_vehiculos(request):
    """
    Función para renderizar la página de vehículos con los datos de modelos.
    """
    URL_API_MODELOS = "https://apitesis.fly.dev/api/v1/Modelo/"
    URL_API_VEHICULOS = "https://apitesis.fly.dev/api/v1/vehiculo/"

    # Obtener modelos
    try:
        response_modelos = requests.get(URL_API_MODELOS)
        if response_modelos.status_code == 200:
            modelos = response_modelos.json()
            print("Modelos:", modelos)  # Verificar en consola
        else:
            modelos = []
            print("Error al obtener modelos")
    except requests.RequestException as e:
        print(f"Error al obtener modelos: {e}")
        modelos = []

    # Obtener vehículos (si también los necesitas en la misma página)
    try:
        response_vehiculos = requests.get(URL_API_VEHICULOS)
        if response_vehiculos.status_code == 200:
            vehiculos = response_vehiculos.json()
        else:
            vehiculos = []
    except requests.RequestException as e:
        print(f"Error al obtener vehículos: {e}")
        vehiculos = []
        
    for vehiculo in vehiculos:
        # Encuentra el modelo correspondiente al vehículo
        vehiculo['modelo_nombre'] = next((modelo['Nombre_Modelo'] for modelo in modelos if modelo['ID_Modelo'] == vehiculo['ID_Modelo']), None)

    return render(request, 'CRUD/vehiculos.html', {'vehiculos': vehiculos, 'modelos': modelos})



def registrar_vehiculo(request):
    
    URL_API = "https://apitesis.fly.dev/api/v1/vehiculo/"  # URL de la API para registrar vehículos

    if request.method == "POST":
        # Capturar los datos enviados desde el formulario
        matricula = request.POST.get("matricula")
        estado_vehiculo = request.POST.get("estado_vehiculo")
        kilometraje = request.POST.get("kilometraje")
        id_modelo = request.POST.get("id_modelo")

        # Crear el objeto JSON con los datos
        data = {
            "Matricula": matricula,
            "Estado_Vehiculo": estado_vehiculo,
            "Kilometraje": kilometraje,
            "Modelo": id_modelo
        }

        try:
            # Enviar los datos a la API
            response = requests.post(URL_API, json=data)

            if response.status_code == 201:
                # Redirigir a la página de listado o mostrar éxito
                return redirect("CRUD/vehiculos.html")  # Ajusta este nombre según tu URL de listado
            else:
                # Manejar errores de la API
                error_message = response.json().get("detail", "Error desconocido")
                return JsonResponse({"error": error_message}, status=response.status_code)

        except requests.RequestException as e:
            # Manejar errores de conexión
            return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

    else:
        # Si no es un POST, renderiza el formulario o regresa un error
        return JsonResponse({"error": "Método no permitido"}, status=405)
    




