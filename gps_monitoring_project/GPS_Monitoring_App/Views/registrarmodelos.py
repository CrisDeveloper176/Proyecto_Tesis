from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
import requests
import json

# Obtener marcas y modelos
def obtener_modelos_y_marcas(request):
    """
    Función para renderizar la página con los datos de modelos y marcas.
    """
    URL_API_MODELOS = "https://apitesis.fly.dev/api/v1/Modelo/"
    URL_API_MARCAS = "https://apitesis.fly.dev/api/v1/Marca/"

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

    # Obtener marcas
    try:
        response_marcas = requests.get(URL_API_MARCAS)
        if response_marcas.status_code == 200:
            marcas = response_marcas.json()
        else:
            marcas = []
    except requests.RequestException as e:
        print(f"Error al obtener marcas: {e}")
        marcas = []

    return render(request, 'CRUD/registrarmodelo.html', {'modelos': modelos, 'marcas': marcas})


def registrar_modelo(request):
    if request.method == "POST":
        # Capturar los datos del formulario
        nombre_modelo = request.POST.get("Nombre_Modelo")
        id_marca = request.POST.get("Id_Marca")  # Aseguramos que id_marca se capture antes de validarlo

        # Validar los campos
        if not nombre_modelo or not id_marca:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

        # Intentar convertir id_marca a entero
        try:
            id_marca = int(id_marca)
        except ValueError:
            return JsonResponse({"error": "El ID de la marca debe ser un número entero válido."}, status=400)

        # Preparar los datos para enviarlos a la API
        data = {
            "Nombre_Modelo": nombre_modelo,
            "Id_Marca": id_marca,
        }
        headers = {
            "Content-Type": "application/json",
        }

        # Enviar la solicitud POST a la API para registrar el modelo
        URL_API = "https://apitesis.fly.dev/api/v1/Modelo/"
        response = requests.post(URL_API, json=data, headers=headers)
        response_data = response.json()
        print("Respuesta de la API:", response_data)

        if response.status_code == 201:
            # Redirigir a la página de modelos
            return redirect("modelos_marcas")  # Ajusta este nombre según tu URL de listado de modelos
        else:
            # Manejar errores de la API
            error_message = response.json().get("detail", "Error al registrar el modelo")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# Editar Modelo
def editar_modelo(request, ID_Modelo):
    if request.method == "POST":
        # Capturar los datos del formulario
        nombre_modelo = request.POST.get("Nombre_Modelo")
        id_marca = request.POST.get("Id_Marca")

        # Validar los campos
        if not nombre_modelo or not id_marca:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
        try:
            id_marca = int(id_marca)
        except ValueError:
            return JsonResponse({"error": "El ID de la marca debe ser un número entero válido."}, status=400)

        # Preparar los datos para enviarlos a la API
        data = {
            "Nombre_Modelo": nombre_modelo,
            "Id_Marca": id_marca,
        }
        headers = {
            "Content-Type": "application/json",
        }

        # URL de la API para editar el modelo
        URL_API = f"https://apitesis.fly.dev/api/v1/Modelo/{ID_Modelo}/"
        response = requests.put(URL_API, json=data, headers=headers)  # Usamos PUT para actualizar
        response_data = response.json()

        if response.status_code == 200:
            # Redirigir a la página de modelos
            return redirect("modelos_marcas")  # Ajusta este nombre según tu URL de listado de modelos
        else:
            # Manejar errores de la API
            error_message = response.json().get("detail", "Error al editar el modelo")
            return JsonResponse({"error": error_message}, status=response.status_code)

    # Si no es POST, mostrar los datos del modelo para editar
    URL_API = f"https://apitesis.fly.dev/api/v1/Modelo/{ID_Modelo}/"
    response = requests.get(URL_API)
    if response.status_code == 200:
        modelo_data = response.json()
        # Aquí devolvemos los datos al modal para rellenarlos
        return JsonResponse({"modelo": modelo_data})
    else:
        return JsonResponse({"error": "Modelo no encontrado"}, status=404)


# Eliminar Modelo
def eliminar_modelo(request, ID_Modelo):
    if request.method == "POST":
        # URL de la API para eliminar el modelo
        URL_API = f"https://apitesis.fly.dev/api/v1/Modelo/{ID_Modelo}/"
        
        # Hacer la solicitud DELETE a la API
        headers = {
            "Content-Type": "application/json",
        }

        try:
            ID_Modelo = int(ID_Modelo)
        except ValueError:
            return JsonResponse({"error": "El ID del modelo debe ser un número válido"}, status=400)
        
        response = requests.delete(URL_API, headers=headers)

        if response.status_code == 204:  # 204 significa que se eliminó correctamente
            return redirect("modelos")  # Redirigir al listado de modelos
        else:
            error_message = response.json().get("detail", "Error al eliminar el modelo")
            return JsonResponse({"error": error_message}, status=response.status_code)

    else:
        return JsonResponse({"error": "Método no permitido"}, status=405)


# Registrar Marca
def registrar_marca(request):
    if request.method == "POST":
        # Capturar los datos del formulario
        nombre_marca = request.POST.get("Nombre_Marca")

        # Validar los campos
        if not nombre_marca:
            return JsonResponse({"error": "El campo Nombre de la Marca es obligatorio"}, status=400)

        # Preparar los datos para enviarlos a la API
        data = {
            "Nombre_Marca": nombre_marca,
        }
        headers = {
            "Content-Type": "application/json",
        }

        # Enviar la solicitud POST a la API para registrar la marca
        URL_API = "https://apitesis.fly.dev/api/v1/Marca/"
        response = requests.post(URL_API, json=data, headers=headers)
        response_data = response.json()
        print("Respuesta de la API:", response_data)

        if response.status_code == 201:
            # Redirigir a la página de marcas
            return redirect("marcas")  # Ajusta este nombre según tu URL de listado de marcas
        else:
            # Manejar errores de la API
            error_message = response.json().get("detail", "Error al registrar la marca")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)
