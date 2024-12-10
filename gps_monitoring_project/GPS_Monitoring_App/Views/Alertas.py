from django.shortcuts import render

def Alerta_view(request):
     return render(request, 'CRUD/AgregarAlerta.html')