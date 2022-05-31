from pyexpat import model
from matplotlib import widgets

from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms



class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrarGastosForm(forms.ModelForm):
    class Meta:
        model = Gastos
        fields = [
            'categoria',
            'recurrencia',
            'nombre',
            'fecha',
            'cantidad',
            'factura'
        ]
        labels = {
            'categoria': '¿Qué tipo de gasto es?',
            'recurrencia': '¿Cada cuánto?',
            'nombre': '¿Qué gasto es?',
            'fecha': '¿Cuándo fue?',
            'cantidad': '¿Cuánto gastaste?',
            'factura': 'Adjunte su factura'
        }
        widgets = {
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'recurrencia': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre gasto'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control','placeholder': 'dd/mm/yyy'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'factura': forms.FileInput(attrs={'class': 'form-control'}),
        }


class RegistrarIngresosForm(forms.ModelForm):
    class Meta:
        model = Ingresos
        fields = [
            'recurrencia',
            'nombre',
            'fecha',
            'cantidad'
        ]
        labels = {
            'recurrencia': '¿Cada cuánto?',
            'nombre': '¿Qué ingreso es?',
            'fecha': '¿Cuándo fue?',
            'cantidad': '¿Cuánto ganaste?',
        }
        widgets = {
            'recurrencia': forms.Select(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre ingreso'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control','placeholder': 'dd/mm/yyy'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

