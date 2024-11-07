# models.py
from django.db import models

class TipoVehiculo(models.Model):
    nombre = models.CharField(max_length=100)

class Combustible(models.Model):
    nombre = models.CharField(max_length=100)

class Vehiculo(models.Model):
    patente = models.CharField(max_length=20, primary_key=True)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.IntegerField()
    tipoVehiculo = models.ForeignKey(TipoVehiculo, on_delete=models.CASCADE)
    combustible = models.ManyToManyField(Combustible)
