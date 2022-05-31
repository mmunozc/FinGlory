
from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
import json

#create your views here

def home(request):
    return render(request, 'home.html')


def inicio(request):
    return render(request, 'inicio.html')


def gastos(request):
    searchTerm = request.GET.get('serchGasto')
    if searchTerm:
        gastos = Gastos.objects.filter(nombre__icontains=searchTerm)
    else:
        gastos = Gastos.objects.all()

    return render(request, 'gastos.html', {'gastos': gastos, 'searchTerm': searchTerm})


def ingresos(request):
    searchTerm = request.GET.get('serchIngreso')
    if searchTerm:
        ingresos = Ingresos.objects.filter(nombre__icontains=searchTerm)
    else:
        ingresos = Ingresos.objects.all()

    return render(request, 'ingresos.html', {'ingresos': ingresos, 'searchTerm': searchTerm})



def registrarGastosView(request, *args, **kwargs):
    if request.method == 'POST':
        if 'crear' in request.POST:
            form = RegistrarGastosForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/gastos/')  # Pendiente a revisar
            else:
                messages.error(request, form.errors)
    else:
        form = RegistrarGastosForm()

    context = {'form': form, 'disabled': (kwargs.get('pk', None) != None), 'nombre_modelo': 'Gasto'}

    return render(request, 'form.html', context)


def registrarIngresosView(request, *args, **kwargs):
    
    if request.method == 'POST':
        if 'crear' in request.POST:
            form = RegistrarIngresosForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/ingresos/')  # Pendiente a revisar
            else:
                messages.error(request, form.errors)
    else:
        form = RegistrarIngresosForm()

    context = {'form': form, 'disabled': (kwargs.get('pk', None) != None), 'nombre_modelo': 'Ingreso'}

    return render(request, 'form.html', context)

def actualizarIngresosView(request, pk):
    instance = get_object_or_404(Ingresos, id=pk)
    if request.method == 'POST':
        form = RegistrarIngresosForm(request.POST, instance=instance)
        
        if form.is_valid():
            form.save()
            return redirect('/ingresos/')  # Pendiente a revisar
        else:
            messages.error(request, form.errors)
    else:
        form = RegistrarIngresosForm(instance=instance)

    context = {'form': form, 'disabled': True, 'nombre_modelo': 'Ingreso'}

    return render(request, 'form.html', context)

def actualizarGastosView(request, pk):
    instance = get_object_or_404(Gastos, id=pk)
    if request.method == 'POST':
            form = RegistrarGastosForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('/gastos/')  # Pendiente a revisar
            else:
                messages.error(request, form.errors)
    else:
        form = RegistrarGastosForm(instance=instance)

    context = {'form': form, 'disabled' : True, 'nombre_modelo': 'Gasto'}

    return render(request, 'form.html', context)

def registrarUsuarioView(request):
    form = MyUserCreationForm()
    if request.method=='POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user= form.save(commit=False)
            user.username= user.username.lower()
            user.save()            
            return redirect('/')
        else: 
            messages.error(request, 'An error occurred during registration')
    
    return render(request,'registroUsuario.html', { 'form' : form})

def estadisticas(request):

    fecha_inicial = request.GET.get('fecha_inicial')
    fecha_final = request.GET.get('fecha_final')
    if fecha_inicial and fecha_final:

        alimentacion = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.alimentacion, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])
        hogar = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.hogar, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])
        entretenimiento = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.entretenimiento, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])
        educacion = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.educacion, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])
        compromisos_bancarios = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.compromisos_bancarios, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])
        otros = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.otros, fecha__gte=fecha_inicial, fecha__lte=fecha_final)])

    else:
        # print("here", flush=True)
        alimentacion = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.alimentacion)])
        hogar = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.hogar)])
        entretenimiento = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.entretenimiento)])
        educacion = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.educacion)])
        compromisos_bancarios = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.compromisos_bancarios)])
        otros = sum([gasto.cantidad for gasto in Gastos.objects.filter(categoria=Gastos.CategoriaGastos.otros)])

    category_data_source = {
        'name': "Distribucion de Gastos",
        "data": []
    }

    category_data_source['data'].append({
       'name': 'Alimentacion',
        'y': alimentacion,
    })
    category_data_source['data'].append({
       'name': 'Hogar',
        'y': hogar,
    })
    category_data_source['data'].append({
       'name': 'Entretenimiento',
        'y': entretenimiento,
    })
    category_data_source['data'].append({
       'name': 'Compromisos Bancarios',
        'y': compromisos_bancarios,
    })
    category_data_source['data'].append({
       'name': 'Educacion',
        'y': educacion,
    })
    category_data_source['data'].append({
       'name': 'Otros',
        'y': otros,
    })


    category_chart_data = {
        'chart': {'type': 'pie'},
        'title': {'text': "Distribucion de Gastos"},
        'setOptions': {
            'lang': {
                'thousandsSep': ','
            }
        },
        'accessibility': {
            'announceNewData': {
                'enabled': True
            }
        },
        'plotOptions': {
            'series': {
                'dataLabels': {
                    'enabled': True,
                    'format': '{point.name}: <br>{point.percentage:.1f} %<br>total: {point.y}',
                    'padding': 0,
                    'style': {
                        'fontSize': '10px'
                    }
                }
            }
        },
        'tooltip': {
            'headerFormat': '<span style="font-size:11px; color:#8e5ea2">{series.name}<br>{point.percentage:.1f} %'
                            '</span><br>',
            'pointFormat': '<span style="color:#3cba9f">{point.name}</span>: <b>{point.y}</b><br/>'
                           
        },
        'series': [category_data_source],
    }
    context = {
        'category_wise_pie_data': json.dumps(category_chart_data)
    }
    return render(request, 'estadisticas.html', context)  

def eliminarIngresosView(request, *args, **kwargs):
    if 'pk' in kwargs:
        pk = kwargs['pk']
        Ingresos.objects.get(pk=pk).delete()
    return redirect('/ingresos/')

def eliminarGastosView(request, *args, **kwargs):
    if 'pk' in kwargs:
        pk = kwargs['pk']
        Gastos.objects.get(pk=pk).delete()
    return redirect('/gastos/')
