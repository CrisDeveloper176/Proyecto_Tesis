from django.shortcuts import render



def visualizar_vehiculo(request):
     return render(request, 'CRUD/RegistrarVehiculo.html')


