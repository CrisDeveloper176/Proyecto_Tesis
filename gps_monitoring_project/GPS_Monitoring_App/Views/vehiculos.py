from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests


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
    if request.method == "POST":
        # Capturar los datos enviados desde el formulario
        matricula = request.POST.get("matricula")
        estado_vehiculo = request.POST.get("estado_vehiculo")
        kilometraje = request.POST.get("kilometraje")
        id_modelo = request.POST.get("id_modelo")

        # Validar los campos
        if not matricula or not estado_vehiculo or not kilometraje or not id_modelo:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
        try:
            kilometraje = int(kilometraje)
        except ValueError:
            return JsonResponse({"error": "El kilometraje debe ser un número entero válido."}, status=400)

        try:
            id_modelo = int(id_modelo)
        except ValueError:
            return JsonResponse({"error": "El ID del modelo debe ser un número entero válido."}, status=400)

        # Preparar los datos para enviarlos a la API
        data = {
            "Matricula": matricula,
            "Estado_Vehiculo": estado_vehiculo,
            "kilometraje": kilometraje,
            "ID_Modelo": id_modelo,
        }
        headers = {
            "Content-Type": "application/json",
            #"Authorization": "Bearer 60XMXnbzk4eybuLoxgj02GxemnCq7AX8b1OmeN5tp "  # Si es necesario
        }
        
        # Enviar la solicitud POST a la API
        URL_API = "https://apitesis.fly.dev/api/v1/vehiculo/"
        response = requests.post(URL_API, json=data,headers=headers)
        response_data = response.json()  # Si la respuesta es JSON
        print("Respuesta de la API:", response_data)  # Muestra el contenido completo  
        if response.status_code == 201:
            # Redirigir a la página de listado o mostrar éxito
            return redirect("vehiculos")  # Ajusta este nombre según tu URL de listado
        else:
            # Manejar errores de la API
            error_message = response.json().get("detail", "Error al registrar el vehículo")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def editar_Vehiculo(request,ID_Vehiculo):
    
   URL_API = f"https://apitesis.fly.dev/api/v1/vehiculo/{ID_Vehiculo}/"  # Ruta de la API con el ID del vehículo

   if request.method == "GET":
        # Obtener los datos del vehículo desde la API para precargar el formulario
        try:
            response = requests.get(URL_API)
            if response.status_code == 200:
                vehiculo = response.json()
                return render(request, "CRUD/editar_vehiculo.html", {"vehiculo": vehiculo})
            else:
                return JsonResponse({"error": "No se pudo obtener los datos del vehículo."}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error al conectar con la API: {e}"}, status=500)

   elif request.method == "POST":
        # Capturar los datos enviados desde el formulario
        matricula = request.POST.get("matricula")
        estado_vehiculo = request.POST.get("estado_vehiculo")
        kilometraje = request.POST.get("kilometraje")
        id_modelo = request.POST.get("id_modelo")

        # Validar los datos
        if not matricula or not estado_vehiculo or not kilometraje or not id_modelo:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

        try:
            kilometraje = int(kilometraje)
            id_modelo = int(id_modelo)
        except ValueError:
            return JsonResponse({"error": "Kilometraje y ID del modelo deben ser números válidos."}, status=400)

        # Preparar los datos para la actualización
        data = {
            "Matricula": matricula,
            "Estado_Vehiculo": estado_vehiculo,
            "kilometraje": kilometraje,
            "ID_Modelo": id_modelo,
        }
        headers = {"Content-Type": "application/json"}

        # Enviar la solicitud PUT a la API para actualizar el vehículo
        try:
            response = requests.put(URL_API, json=data, headers=headers)
            if response.status_code == 200:
                # Redirigir a la lista de vehículos después de editar
                return redirect('listar_vehiculos')
            else:
                error_message = response.json().get("detail", "Error al actualizar el vehículo.")
                return JsonResponse({"error": error_message}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error al conectar con la API: {e}"}, status=500)

   return JsonResponse({"error": "Método no permitido"}, status=405)
        
                
    
