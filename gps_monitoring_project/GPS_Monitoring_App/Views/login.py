from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
@login_required(login_url='TemplatesBase/login/')
def home(request):
       return render(request, 'TemplatesBase/Home.html')

@csrf_exempt  # Desactiva la verificación de CSRF para esta vista
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # Autenticación interna usando Django's authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Si la autenticación es exitosa, inicias sesión
            auth_login(request, user)

            # Redirige al home o a la página principal después de login
            return redirect('TemplatesBase/Home.html')
        else:
            # Si las credenciales son incorrectas
            return JsonResponse({'error': 'Credenciales inválidas'}, status=401)

    return render(request, 'TemplatesBase/Login.html')
