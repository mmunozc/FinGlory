from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=200, null=False)
    email= models.EmailField(unique=True, null=False)
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS=[]


class Gastos(models.Model):
    class TipoRecurrencia(models.TextChoices):
        mensual = 'Mensual'
        anual = 'Anual'
        no_recurrente = 'No recurente'
        
    class  CategoriaGastos(models.TextChoices):
        alimentacion = 'Alimentación'
        hogar = 'Hogar'
        entretenimiento = 'Entretenimiento'
        educacion = 'Educación'
        compromisos_bancarios = 'Compromisos Bancarios'
        otros = 'Otros'
    categoria = models.CharField(max_length=30, choices = CategoriaGastos.choices, default = CategoriaGastos.otros )
    recurrencia = models.CharField(max_length=20, choices = TipoRecurrencia.choices, default = TipoRecurrencia.mensual)
    nombre = models.CharField(max_length=30, null=False)
    fecha = models.DateField(null=False, blank=True)
    cantidad = models.IntegerField(default=0, blank=True, null=False)
    factura = models.ImageField(upload_to = 'app/images/', blank=True)
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Ingresos(models.Model):    
    class TipoRecurrencia(models.TextChoices):
        mensual = 'Mensual'
        anual = 'Anual'
        no_recurrente = 'No recurrente'

    recurrencia = models.CharField(max_length=20, choices = TipoRecurrencia.choices, default = TipoRecurrencia.mensual)
    nombre = models.CharField(max_length=30, null=False)
    fecha = models.DateField(null=False, blank=True) 
    cantidad = models.IntegerField(default=0, blank=True, null=False)


