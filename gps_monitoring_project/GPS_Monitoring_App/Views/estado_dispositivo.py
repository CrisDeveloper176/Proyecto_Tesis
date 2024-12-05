from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

# URL base de la API (ajústala según tus necesidades)
URL_API_ESTADO_GPS = "https://apitesis.fly.dev/api/v1/Estado_GPS/"

def listar_estados_gps(request):
    """Obtener y mostrar la lista de Estados GPS."""
    try:
        response = requests.get(URL_API_ESTADO_GPS)
        estados = response.json() if response.status_code == 200 else []
    except requests.RequestException as e:
        print(f"Error al obtener estados GPS: {e}")
        estados = []

    return render(request, 'CRUD/estado_dispositivo.html', {'Estados': estados})

def registrar_estado_gps(request):
    """Registrar un nuevo Estado GPS."""
    if request.method == "POST":
        estado = request.POST.get("estado")
        if not estado:
            return JsonResponse({"error": "El campo estado es obligatorio."}, status=400)

        data = {"Estado": estado}
        try:
            response = requests.post(URL_API_ESTADO_GPS, json=data)
            if response.status_code == 201:
                return redirect('estadoGps')
            else:
                return JsonResponse({"error": "Error al registrar el estado GPS."}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

def editar_estado_gps(request, ID_EstadoGps):
    """Editar un Estado GPS existente."""
    if request.method == "POST":
        estado = request.POST.get("estado")
        if not estado:
            return JsonResponse({"error": "El campo estado es obligatorio."}, status=400)

        data = {"Estado": estado}
        try:
            url = f"{URL_API_ESTADO_GPS}{ID_EstadoGps}/"
            response = requests.put(url, json=data)
            if response.status_code == 200:
                return redirect('estadoGps')
            else:
                return JsonResponse({"error": "Error al editar el estado GPS."}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

def eliminar_estado_gps(request, ID_EstadoGps):
    """Eliminar un Estado GPS."""
    if request.method == "POST":
        try:
            url = f"{URL_API_ESTADO_GPS}{ID_EstadoGps}/"
            response = requests.delete(url)
            if response.status_code == 204:
                return redirect('estadoGps')
            else:
                return JsonResponse({"error": "Error al eliminar el estado GPS."}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)
