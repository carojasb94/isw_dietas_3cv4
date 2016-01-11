from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from apps.nutriologo.forms import agendar_cita_form, crear_dieta_form


@login_required
def agendar_cita(request):
    print('agendar_cita')
    print(request)
    if request.method == 'POST':
        print(request.POST)
        formulario = agendar_cita_form(request.POST)
        if formulario.is_valid():
            print('formulario valido')

            return render(request, 'nutriologo/agendar_cita.html', {'success':True})

    return render(request, 'nutriologo/agendar_cita.html', {'success':False})


def crear_dieta(request):
    print('crear_dieta')
    print(request)
    if request.method == 'POST':
        print(request.POST)
        formulario_dieta = crear_dieta_form(request.POST)
        if formulario_dieta.is_valid():
            print('formulario valido')


        return render(request, 'nutriologo/crear_dieta.html', {'success':True})

    return render(request, 'nutriologo/crear_dieta.html', {'success':False})






