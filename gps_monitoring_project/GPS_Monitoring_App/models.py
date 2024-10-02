from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()

class RastreoGPS(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    latitud = models.FloatField()
    longitud = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.latitud}, {self.longitud} at {self.timestamp}"