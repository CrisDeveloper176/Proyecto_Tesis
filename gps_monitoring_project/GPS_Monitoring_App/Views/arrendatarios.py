from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse





def format_rut(rut):
    """
    Formatea un RUT al formato XX.XXX.XXX-X.
    """
    rut = rut.replace(".", "").replace("-", "")  
    if len(rut) < 2:
        return rut  
    body = f"{int(rut[:-1]):,}".replace(",", ".")  
    verifier = rut[-1].upper()  
    return f"{body}-{verifier}"



def obtener_arrendatarios(request):
    URL_API_ARRENDATARIOS = "https://apitesis.fly.dev/api/v1/arrendatarios/"
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
        rut = request.POST.get("rut")
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        licencia = request.POST.get("licencia")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")

        if not nombre or not correo or not telefono:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

        try:
            telefono = int(telefono)
        except ValueError:
            return JsonResponse({"error": "El teléfono debe ser un número entero válido."}, status=400)

        data = {
            "Rut": rut,
            "Nombre": nombre,
            "Apellido": apellido,
            "Licencia_Conducir": licencia,
            "Telefono": telefono,
            "Correo": correo,
        }
        headers = {"Content-Type": "application/json"}

        URL_API = "https://apitesis.fly.dev/api/v1/arrendatarios/"
        try:
            response = requests.post(URL_API, json=data, headers=headers)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error al conectar con la API: {e}"}, status=500)

        if response.status_code == 201:
            return redirect("arrendatario")
        else:
            error_message = response.json().get("detail", "Error al registrar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)

def editar_arrendatario(request, rut):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        licencia = request.POST.get("licencia")
        telefono = request.POST.get("telefono")
        correo = request.POST.get("correo")

        if not nombre or not correo or not telefono:
            return JsonResponse({"error": "Todos los campos son obligatorios"}, status=400)

        data = {
            "Rut": rut,
            "Nombre": nombre,
            "Apellido": apellido,
            "Licencia_Conducir": licencia,
            "Telefono": telefono,
            "Correo": correo,
        }
        headers = {"Content-Type": "application/json"}

        URL_API = f"https://apitesis.fly.dev/api/v1/arrendatarios/{rut}/"
        try:
            response = requests.put(URL_API, json=data, headers=headers)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error al conectar con la API: {e}"}, status=500)

        if response.status_code == 200:
            return redirect("arrendatario")
        elif response.status_code == 404:
            return JsonResponse({"error": "El arrendatario no fue encontrado en la base de datos."}, status=404)
        else:
            error_message = response.json().get("detail", "Error al editar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

def eliminar_arrendatario(request, rut):
    if request.method == "POST":
        URL_API = f"https://apitesis.fly.dev/api/v1/arrendatarios/{rut}/"
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.delete(URL_API, headers=headers)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error al conectar con la API: {e}"}, status=500)

        if response.status_code == 204:
            return redirect("arrendatario")
        elif response.status_code == 404:
            return JsonResponse({"error": "El arrendatario no fue encontrado en la base de datos."}, status=404)
        else:
            error_message = response.json().get("detail", "Error al eliminar el arrendatario")
            return JsonResponse({"error": error_message}, status=response.status_code)

    return JsonResponse({"error": "Método no permitido"}, status=405)
