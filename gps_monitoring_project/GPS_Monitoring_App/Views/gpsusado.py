from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from datetime import datetime
import pytz

# URLs base de la API
URL_API_DISPOSITIVO_GPS = "https://apitesis.fly.dev/api/v1/Dispositivo_GPS/"
URL_API_GPS_USADOS = "https://apitesis.fly.dev/api/v1/GPSUsados/"
URL_API_VEHICULOS = "https://apitesis.fly.dev/api/v1/vehiculo/"

def listar_dispositivos_gps_usados(request):
    """Obtener y mostrar la lista de dispositivos GPS usados."""
    try:
        dispositivos_response = requests.get(URL_API_GPS_USADOS)
        dispositivos = dispositivos_response.json() if dispositivos_response.status_code == 200 else []

        # Formatear las fechas en el formato año/mes/día hora:minutos
        for dispositivo in dispositivos:
            for campo_fecha in ["fecha_Instalacion", "fecha_Deceso"]:
                if dispositivo.get(campo_fecha):
                    dispositivo[campo_fecha] = datetime.fromisoformat(
                        dispositivo[campo_fecha].replace("Z", "+00:00")
                    ).astimezone(pytz.timezone("America/Santiago")).strftime("%Y/%m/%d %H:%M")
                else:
                    dispositivo[campo_fecha] = None

        vehiculos_response = requests.get(URL_API_VEHICULOS)
        vehiculos = vehiculos_response.json() if vehiculos_response.status_code == 200 else []

        imei_response = requests.get(URL_API_DISPOSITIVO_GPS)
        imeis_data = imei_response.json() if imei_response.status_code == 200 else []
        imeis = [item.get("imei") for item in imeis_data if item.get("imei")]

        for dispositivo in dispositivos:
            vehiculo_id = dispositivo.get("ID_Vehiculo")
            dispositivo["Vehiculo"] = next(
                (vehiculo for vehiculo in vehiculos if vehiculo["ID_Vehiculo"] == vehiculo_id),
                {"Matricula": "No asignado", "ID_Vehiculo": "N/A"}
            )

    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        dispositivos, vehiculos, imeis = [], [], []

    return render(request, 'CRUD/gpsusado.html', {
        'Dispositivos': dispositivos,
        'Vehiculos': vehiculos,
        'IMEIs': imeis,
    })

def registrar_dispositivo_gps_usado(request):
    """Registrar un nuevo dispositivo GPS usado."""
    try:
        imei_response = requests.get(URL_API_DISPOSITIVO_GPS)
        imeis_data = imei_response.json() if imei_response.status_code == 200 else []
        imeis = [item.get("imei") for item in imeis_data if item.get("imei")]

        vehiculos_response = requests.get(URL_API_VEHICULOS)
        vehiculos = vehiculos_response.json() if vehiculos_response.status_code == 200 else []

        # Verificar si el IMEI ya está asignado a un vehículo
        imei_asignado = None
        if request.method == "POST":
            imei = request.POST.get("imei")
            vehiculo_id = request.POST.get("ID_Vehiculo_id")

            # Validar si el IMEI ya está registrado en otro vehículo
            dispositivos_response = requests.get(URL_API_GPS_USADOS)
            dispositivos = dispositivos_response.json() if dispositivos_response.status_code == 200 else []
            for dispositivo in dispositivos:
                if dispositivo['ID_GPS'] == imei and dispositivo['ID_Vehiculo'] != vehiculo_id:
                    imei_asignado = dispositivo['ID_Vehiculo']
                    break

            if imei_asignado:
                return JsonResponse({"error": f"Este IMEI ya está asignado a otro vehículo (ID: {imei_asignado})."}, status=400)

            # Obtener la fecha y hora actual en la zona horaria de Chile
            chile_timezone = pytz.timezone('America/Santiago')
            fecha_instalacion = datetime.now(chile_timezone).isoformat(timespec='seconds')

            if not imei or not vehiculo_id:
                return JsonResponse({"error": "Los campos IMEI y Vehículo son obligatorios."}, status=400)

            data = {
                "fecha_Instalacion": fecha_instalacion,
                "ID_GPS": imei,
                "ID_Vehiculo": vehiculo_id,
            }
            headers = {"Content-Type": "application/json"}

            try:
                response = requests.post(URL_API_GPS_USADOS, json=data, headers=headers)
                if response.status_code == 201:
                    return redirect('gpsusado')
                return JsonResponse({
                    "error": f"Error: {response.json().get('detail', 'Desconocido')}."
                }, status=response.status_code)
            except requests.RequestException as e:
                return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

        # Calcular la fecha actual para mostrar en el modal
        chile_timezone = pytz.timezone('America/Santiago')
        fecha_instalacion = datetime.now(chile_timezone).strftime("%Y-%m-%dT%H:%M")

    except requests.RequestException as e:
        print(f"Error al cargar datos: {e}")
        imeis, vehiculos = [], []

    return render(request, 'CRUD/registrar_gpsusado.html', {
        'IMEIs': imeis,
        'Vehiculos': vehiculos,
        'FechaInstalacion': fecha_instalacion,
    })


def editar_dispositivo_gps_usado(request, imei):
    """Editar un dispositivo GPS usado existente."""
    try:
        # Obtener información actual del dispositivo
        dispositivo_response = requests.get(f"{URL_API_GPS_USADOS}{imei}/")
        dispositivo = dispositivo_response.json() if dispositivo_response.status_code == 200 else None

        # Obtener lista de vehículos
        vehiculos_response = requests.get(URL_API_VEHICULOS)
        vehiculos = vehiculos_response.json() if vehiculos_response.status_code == 200 else []

        # Obtener lista de IMEIs
        imei_response = requests.get(URL_API_DISPOSITIVO_GPS)
        imeis_data = imei_response.json() if imei_response.status_code == 200 else []
        imeis = [item.get("imei") for item in imeis_data if item.get("imei")]

    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        dispositivo, vehiculos, imeis = None, [], []

    if request.method == "POST":
        # Datos recibidos del formulario
        fecha_deceso = request.POST.get("fecha_Deceso")
        vehiculo_id = request.POST.get("ID_Vehiculo_id")

        # Validar campos obligatorios
        if not vehiculo_id:
            return JsonResponse({"error": "El campo Vehículo es obligatorio."}, status=400)

        # Verificar si el IMEI ya está asignado a otro vehículo
        dispositivos_response = requests.get(URL_API_GPS_USADOS)
        dispositivos = dispositivos_response.json() if dispositivos_response.status_code == 200 else []
        for dispositivo in dispositivos:
            if dispositivo['ID_GPS'] == imei and dispositivo['ID_Vehiculo'] != vehiculo_id:
                return JsonResponse({"error": f"Este IMEI ya está asignado a otro vehículo (ID: {dispositivo['ID_Vehiculo']})."}, status=400)

        # Construir datos para el PUT
        data = {
            "ID_GPS": imei,  # El IMEI es obligatorio
            "fecha_Instalacion": dispositivo["fecha_Instalacion"],  # Mantener la fecha de instalación original
            "fecha_Deceso": fecha_deceso or None,  # Puede ser opcional
            "ID_Vehiculo": vehiculo_id,  # Nuevo vehículo asignado
        }

        headers = {"Content-Type": "application/json"}

        try:
            # Enviar solicitud PUT a la API
            response = requests.put(f"{URL_API_GPS_USADOS}{imei}/", json=data, headers=headers)
            if response.status_code == 200:
                return redirect('gpsusado')  # Redirigir al listado después de la edición
            else:
                # Mostrar error si la API responde con un estado diferente a 200
                error_message = response.json().get("detail", "Error desconocido")
                return JsonResponse({"error": error_message}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

    return render(request, 'CRUD/editar_gpsusado.html', {
        'Dispositivo': dispositivo,
        'Vehiculos': vehiculos,
        'IMEIs': imeis,
    })
