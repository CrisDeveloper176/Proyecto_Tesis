from django.shortcuts import render
import requests

def vehiculos(request):
    api_url = 'http://localhost:5168/Vehiculos'
    tipos_api_url = 'http://localhost:5168/TipoVehiculo'
    combustibles_api_url = 'http://localhost:5168/Combustible'

    try:
        response = requests.get(api_url)
        vehiculos = response.json()
        
        # Obtener tipos de vehículo
        response_tipos = requests.get(tipos_api_url)
        tipos_vehiculo = response_tipos.json()

        # Obtener combustibles
        response_combustibles = requests.get(combustibles_api_url)
        combustibles = response_combustibles.json()

    except requests.exceptions.RequestException as e:
        vehiculos = []
        tipos_vehiculo = []
        combustibles = []

    return render(request, 'create_vehiculo', {
        'vehiculos': vehiculos,
        'tipos_vehiculo': tipos_vehiculo,
        'combustibles': combustibles,
    })

def create_vehiculo(request):
    if request.method == 'POST':
        data = {
            "patente": request.POST.get('patente'),
            "marca": request.POST.get('marca'),
            "modelo": request.POST.get('modelo'),
            "anio": request.POST.get('anio'),
            "tipoVehiculo": request.POST.get('tipoVehiculo'),
            "combustible": request.POST.getlist('combustible')  # Múltiples combustibles
        }
        
        api_url = 'http://localhost:5168/Vehiculos'
        try:
            response = requests.post(api_url, json=data)
            if response.status_code == 201:
                return vehiculos(request)  # Redirigir a la lista de vehículos
            else:
                return render(request, 'vehiculos', {'vehiculos': [], 'error': 'Error al crear el vehículo.'})
        except requests.exceptions.RequestException as e:
            return render(request, 'vehiculos', {'vehiculos': [], 'error': str(e)})
    
    return render(request, 'vehiculos.html', {'vehiculos': []})
    response = requests.get('http://localhost:5168/Vehiculos')
    return JsonResponse(response.json(), safe=False)
def get_vehiculos(request):
    api_url = 'http://localhost:5168/Vehiculos'
    try:
        response = requests.get(api_url)
        vehiculos = response.json()
        return render(request, 'vehiculos_list.html', {'vehiculos': vehiculos})
    except requests.exceptions.RequestException as e:
        return render(request, 'vehiculos_list.html', {'error': str(e)})
def get_vehiculo_by_id(request, vehiculo_id):
    api_url = f'http://localhost:5168/Vehiculos/{vehiculo_id}'
    try:
        response = requests.get(api_url)
        vehiculo = response.json()
        return render(request, 'vehiculo_detail.html', {'vehiculo': vehiculo})
    except requests.exceptions.RequestException as e:
        return render(request, 'vehiculo_detail.html', {'error': str(e)})

def update_vehiculo(request, vehiculo_id):
    if request.method == 'POST':
        data = {
            "patente": request.POST.get('patente'),
            "marca": request.POST.get('marca'),
            "modelo": request.POST.get('modelo'),
            "anio": request.POST.get('anio'),
            "tipoVehiculo": request.POST.get('tipoVehiculo'),
            "combustible": request.POST.get('combustible')
        }
        api_url = f'http://localhost:5168/Vehiculos/{vehiculo_id}'
        try:
            response = requests.put(api_url, json=data)
            if response.status_code == 200:
                return render(request, 'update_vehiculo.html', {'success': True})
            else:
                error_message = response.json().get('error', 'Error al actualizar vehículo.')
                return render(request, 'update_vehiculo.html', {'error': error_message})
        except requests.exceptions.RequestException as e:
            return render(request, 'update_vehiculo.html', {'error': str(e)})
    
    # Renderiza el formulario vacío si es una solicitud GET
    return render(request, 'update_vehiculo.html')
def delete_vehiculo(request, vehiculo_id):
    api_url = f'http://localhost:5168/Vehiculos/{vehiculo_id}'
    try:
        response = requests.delete(api_url)
        if response.status_code == 204:
            return render(request, 'delete_vehiculo.html', {'success': True})
        else:
            error_message = response.json().get('error', 'Error al eliminar vehículo.')
            return render(request, 'delete_vehiculo.html', {'error': error_message})
    except requests.exceptions.RequestException as e:
        return render(request, 'delete_vehiculo.html', {'error': str(e)})
