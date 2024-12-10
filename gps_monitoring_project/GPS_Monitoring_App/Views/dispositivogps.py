from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
import django

URL_API_DISPOSITIVO_GPS = "https://apitesis.fly.dev/api/v1/Dispositivo_GPS/"
URL_API_ESTADO_GPS = "https://apitesis.fly.dev/api/v1/Estado_GPS/"

def listar_dispositivos_gps(request):
    """Obtener y mostrar la lista de dispositivos GPS."""
    try:

        dispositivos_response = requests.get(URL_API_DISPOSITIVO_GPS)
        dispositivos = dispositivos_response.json() if dispositivos_response.status_code == 200 else []

        estados_response = requests.get(URL_API_ESTADO_GPS)
        estados = estados_response.json() if estados_response.status_code == 200 else []

        for dispositivo in dispositivos:
            estado_id = dispositivo.get("ID_EstadoGps_id")
            dispositivo["Estado"] = next(
                (estado["Estado"] for estado in estados if estado["ID_EstadoGps"] == estado_id),
                "Desconocido"
            )
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        dispositivos = []
        estados = []

    return render(request, 'CRUD/dispositivogps.html', {
        'Dispositivos': dispositivos,
        'Estados': estados
    })





from django.contrib import messages

def registrar_dispositivo_gps(request):
    if request.method == "POST":
        imei = request.POST.get("imei")
        estado_id = request.POST.get("estado_id")

        if not imei or not estado_id:
            messages.error(request, "El campo IMEI y el Estado son obligatorios.")
            return redirect('dispositivoGps')

        try:
            estado_id = int(estado_id)
        except ValueError:
            messages.error(request, "El ID del Estado debe ser un número válido.")
            return redirect('dispositivoGps')

        data = {"imei": imei, "ID_EstadoGps_id": estado_id}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(URL_API_DISPOSITIVO_GPS, json=data, headers=headers)
            if response.status_code == 201:
                messages.success(request, "Dispositivo registrado exitosamente.")
            else:
                error_message = response.json().get("detail", "Error desconocido")
                messages.error(request, f"Error al registrar el dispositivo: {error_message}")
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión: {str(e)}")

        return redirect('dispositivoGps')



def obtener_estados_por_dispositivo(request, ID_DispositivoGps):
    """Obtener la lista de estados GPS para un dispositivo por su ID."""
    try:
        url = f"{URL_API_ESTADO_GPS}?dispositivo_id={ID_DispositivoGps}"  
        response = requests.get(url)
        estados = response.json() if response.status_code == 200 else []
    except requests.RequestException as e:
        print(f"Error al obtener estados del dispositivo GPS: {e}")
        estados = []

    return render(request, 'CRUD/dispositivogps.html', {'Estados': estados, 'DispositivoID': ID_DispositivoGps})


def obtener_dispositivos_y_estados(request):
    """Obtener dispositivos GPS y sus estados relacionados."""
    try:
        dispositivos_response = requests.get(URL_API_DISPOSITIVO_GPS)
        dispositivos = dispositivos_response.json() if dispositivos_response.status_code == 200 else []

        estados_response = requests.get(URL_API_ESTADO_GPS)
        estados = estados_response.json() if estados_response.status_code == 200 else []

        for dispositivo in dispositivos:
            dispositivo['Estados'] = [
                estado for estado in estados if estado.get('dispositivo_id') == dispositivo.get('ID_DispositivoGps')
            ]
    except requests.RequestException as e:
        print(f"Error al obtener dispositivos o estados: {e}")
        dispositivos = []

    return render(request, 'CRUD/dispositivogps.html', {'Dispositivos': dispositivos})




def editar_dispositivo_gps(request, imei):
    if request.method == "POST":
        nuevo_imei = request.POST.get("imei")
        estado_id = request.POST.get("estado_id")

        if not nuevo_imei or not estado_id:
            messages.error(request, "El campo IMEI y el Estado son obligatorios.")
            return redirect('dispositivoGps')

        try:
            estado_id = int(estado_id)
        except ValueError:
            messages.error(request, "El ID del Estado debe ser un número válido.")
            return redirect('dispositivoGps')

        data = {"imei": nuevo_imei, "ID_EstadoGps_id": estado_id}
        headers = {"Content-Type": "application/json"}

        try:
            url = f"{URL_API_DISPOSITIVO_GPS}{imei}/"
            response = requests.put(url, json=data, headers=headers)

            if response.status_code == 200:
                messages.success(request, "Dispositivo actualizado correctamente.")
            else:
                error_message = response.json().get("detail", "Error desconocido")
                messages.error(request, f"Error al editar el dispositivo: {error_message}")
        except requests.RequestException as e:
            messages.error(request, f"Error de conexión: {str(e)}")

        return redirect('dispositivoGps')




def eliminar_dispositivo_gps(request, imei):
    """Eliminar un dispositivo GPS existente."""
    if request.method == "POST":
        try:
            url = f"{URL_API_DISPOSITIVO_GPS}{imei}/"
            response = requests.delete(url)

            if response.status_code == 204:
                messages.success(request, f"El dispositivo IMEI fue eliminado exitosamente.")
            else:
                error_message = response.json().get("detail", "Ocurrió un problema inesperado al intentar eliminar el dispositivo.")
                messages.error(request, f"No se pudo eliminar el dispositivo con IMEI {imei}: {error_message}")
        except requests.RequestException as e:
            messages.error(request, f"No se puede eliminar IMEI que esta asignado")
        except ValueError:
            messages.error(request, "Se recibió una respuesta inesperada del servidor al intentar eliminar el dispositivo.")
        return redirect('dispositivoGps')

    messages.error(request, "Operación no permitida. Por favor, utiliza un método válido para realizar esta acción.")
    return redirect('dispositivoGps')



