from django.shortcuts import render

def TipoMantenimiento_view(request):
     return render(request, 'CRUD/TipoMantenimiento.html')