from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests

def Reportes(request):
     return render(request, 'Reportes/Reportes.html')