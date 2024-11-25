from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse



def obtener_arrendatarios(request):
    """
    Función para renderizar la página de arrendatarios con los datos obtenidos de la API.
    """
    URL_API_ARRENDATARIOS = "https://apitesis.fly.dev/api/v1/Arrendatarios/"

    # Obtener arrendatarios
    try:
        response_arrendatarios = requests.get(URL_API_ARRENDATARIOS)
        if response_arrendatarios.status_code == 200:
            arrendatarios = response_arrendatarios.json()
        else:
            arrendatarios = []
            print("Error al obtener arrendatarios")
    except requests.RequestException as e:
        print(f"Error al obtener arrendatarios: {e}")
        arrendatarios = []

    return render(request, 'CRUD/arrendatarios.html', {'arrendatarios': arrendatarios})


def registrar_arrendatario(request):
    if request.method == "POST":
        # Capturar datos del formulario
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        licencia = request.POST.get("licencia")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")
        

        # Validar campos
        if not nombre or not rut or not correo or not telefono:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)
        
        try:
            telefono = int(telefono)
        except ValueError:
            return JsonResponse({"error": "El telefono debe ser un número entero válido."}, status=400)

        # Preparar los datos para la API
        data = {
            "Rut": rut,
            "Nombre": nombre,
            "Apellido": apellido,
            "Licencia_Conducir": licencia,
            "Telefono": telefono,
            "Correo": correo,
        }
        headers = {
            "Content-Type": "application/json",
            #"Authorization": "Bearer 60XMXnbzk4eybuLoxgj02GxemnCq7AX8b1OmeN5tp "  # Si es necesario
        }

        # Enviar la solicitud POST a la API
        URL_API = "https://apitesis.fly.dev/api/v1/Arrendatarios/"
        response = requests.post(URL_API, json=data,headers=headers)
        response_data = response.json()  # Si la respuesta es JSON
        print("Respuesta de la API:", response_data)  # Muestra el contenido completo  
        if response.status_code == 201:
            # Redirigir a la página de listado o mostrar éxito
            return redirect("arrendatario")  # Usa el nombre correcto de la URL en urls.py
        else:
            # Manejar errores de la API
            error_message = response.json().get("detail", "Error al registrar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def editar_arrendatario(request, id):
    if request.method == "POST":
        # Capturar datos del formulario
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        licencia = request.POST.get("licencia")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")

        # Validar campos
        if not nombre or not rut or not correo or not telefono:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

        # Preparar datos para la API
        data = {
            "Rut": rut,
            "Nombre": nombre,
            "Apellido": apellido,
            "Licencia_Conducir": licencia,
            "Telefono": telefono,
            "Correo": correo,
        }
        headers = {"Content-Type": "application/json"}

        # Enviar solicitud PUT a la API
        URL_API = f"https://apitesis.fly.dev/api/v1/Arrendatarios/{id}/"
        response = requests.put(URL_API, json=data, headers=headers)

        if response.status_code == 200:
            return redirect("arrendatario")
        else:
            error_message = response.json().get("detail", "Error al editar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

    # Si no es POST, obtener datos del arrendatario
    URL_API = f"https://apitesis.fly.dev/api/v1/Arrendatarios/{id}/"
    response = requests.get(URL_API)
    if response.status_code == 200:
        arrendatario_data = response.json()
        return JsonResponse({"arrendatario": arrendatario_data})
    else:
        return JsonResponse({"error": "Arrendatario no encontrado"}, status=404)


def eliminar_arrendatario(request, id):
    if request.method == "POST":
        # URL de la API para eliminar arrendatarios
        URL_API = f"https://apitesis.fly.dev/api/v1/Arrendatarios/{id}/"
        headers = {"Content-Type": "application/json"}

        # Enviar solicitud DELETE a la API
        response = requests.delete(URL_API, headers=headers)

        if response.status_code == 204:
            return redirect("arrendatario")
        else:
            error_message = response.json().get("detail", "Error al eliminar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)
