from django.shortcuts import render

def Mantenimiento_view(request):
     return render(request, 'CRUD/Mantenimiento.html')