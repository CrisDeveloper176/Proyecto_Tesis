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





def registrar_dispositivo_gps(request):
    """Registrar un nuevo dispositivo GPS."""
    if request.method == "POST":
        imei = request.POST.get("imei")
        estado_id = request.POST.get("estado_id")

        if not imei or not estado_id:
            return JsonResponse({"error": "El campo IMEI y el Estado son obligatorios."}, status=400)

        try:
            estado_id = int(estado_id) 
        except ValueError:
            return JsonResponse({"error": "El ID del Estado debe ser un número entero válido."}, status=400)

        data = {
            "imei": imei,
            "ID_EstadoGps_id": estado_id
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(URL_API_DISPOSITIVO_GPS, json=data, headers=headers)
            print("Respuesta de la API:", response.status_code, response.text)

            if response.status_code == 201:
                return redirect('dispositivoGps')  
            else:
                try:
                    error_message = response.json().get("detail", "Error desconocido")
                except ValueError:  
                    error_message = "La API devolvió un cuerpo no JSON."
                return JsonResponse({"error": f"Error al registrar el dispositivo GPS: {error_message}"}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido."}, status=405)


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
    """Editar un dispositivo GPS existente."""
    if request.method == "POST":
        nuevo_imei = request.POST.get("imei")
        estado_id = request.POST.get("estado_id")

        if not nuevo_imei or not estado_id:
            return JsonResponse({"error": "El campo IMEI y el Estado son obligatorios."}, status=400)

        try:
            estado_id = int(estado_id) 
        except ValueError:
            return JsonResponse({"error": "El ID del Estado debe ser un número entero válido."}, status=400)

        data = {
            "imei": nuevo_imei,
            "ID_EstadoGps_id": estado_id
        }

        headers = {
            "Content-Type": "application/json"
        }

        # Verificar la existencia del dispositivo antes de editar
        try:

            url = f"{URL_API_DISPOSITIVO_GPS}{imei}/"
            get_response = requests.get(url)  # Realizar una solicitud GET al recurso

            if get_response.status_code == 404:
                return JsonResponse({"error": f"El dispositivo GPS con IMEI {imei} no existe."}, status=404)

            # Realizar la solicitud de edición con PUT
            put_response = requests.put(url, json=data, headers=headers)

            if put_response.status_code == 200:  # Actualización exitosa
                return redirect('dispositivoGps')

            url = f"{URL_API_DISPOSITIVO_GPS}{imei}/"  
            response = requests.put(url, json=data, headers=headers)

            if response.status_code == 200:
                return redirect('dispositivoGps') 

            else:
                # Manejar errores de la API en la edición
                try:
                    error_message = put_response.json().get("detail", "Error desconocido")
                except ValueError:  # Si la respuesta no es JSON
                    error_message = "La API devolvió un cuerpo no JSON."
                return JsonResponse({"error": f"Error al editar el dispositivo GPS: {error_message}"}, status=put_response.status_code)

        except requests.RequestException as e:
            return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido."}, status=405)




def eliminar_dispositivo_gps(request, imei):
    """Eliminar un dispositivo GPS existente."""
    if request.method == "POST":
        try:
            url = f"{URL_API_DISPOSITIVO_GPS}{imei}/"  
            response = requests.delete(url)

            if response.status_code == 204:  
                return redirect('dispositivoGps')  
            else:
                error_message = response.json().get("detail", "Error desconocido")
                return JsonResponse({"error": f"Error al eliminar el dispositivo GPS: {error_message}"}, status=response.status_code)
        except requests.RequestException as e:
            return JsonResponse({"error": f"Error de conexión: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido."}, status=405)





