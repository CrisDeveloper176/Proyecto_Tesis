from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
    nombre = models.CharField(max_length=100)
    latitud = models.FloatField()
    longitud = models.FloatField()

    def __str__(self):
        return self.nombre