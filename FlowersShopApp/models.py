from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser): 
    celular = models.CharField(max_length=10)
    direccion = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.username

class Flowers(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    descripcion = models.CharField(max_length=300, default="")
    imagen = models.ImageField(upload_to="flowers/", default="")

    def __str__(self):
        return self.nombre

