from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests

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
