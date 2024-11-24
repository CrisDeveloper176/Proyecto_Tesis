from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse
import json
import requests


def Arrendatarios(request):
    return render(request, 'CRUD/arrendatarios.html')