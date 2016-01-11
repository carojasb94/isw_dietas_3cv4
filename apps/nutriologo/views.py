from django.shortcuts import render

# Create your views here.
from apps.nutriologo.forms import agendar_cita_form


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







