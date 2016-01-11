from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect

# Create your views here.
from apps.nutriologo.forms import agendar_cita_form, crear_dieta_form
from apps.nutriologo.models import Cita, Dieta
from apps.usuarios.models import Usuario


@login_required
def agendar_cita(request):
    print('agendar_cita')
    print(request)
    if request.method == 'POST':
        print(request.POST)

        if 'mensaje' in request.POST:
            print('post del formulario de la cita')
            formulario = agendar_cita_form(request.POST)

            if formulario.is_valid():
                print('formulario valido')
                if 'id_nutriologo' in request.session:
                    id_nutriologo = request.session['id_nutriologo']
                    nutriologo = Usuario.objects.get(id=id_nutriologo)
                    cita = Cita.objects.create(nutriologo=nutriologo,
                                               paciente = request.user,
                                               mensaje = formulario.cleaned_data['mensaje'],
                                               fecha = formulario.cleaned_data['fecha'],
                                               status = 'pendiente')
                    print('se creo sin problemas la cita')
                    #eliminamos variable de session
                    del request.session['id_nutriologo']
                    return redirect(reverse('usuarios_app:perfil_paciente',kwargs={'username':request.user.username}) )

            else:
                return render(request, 'nutriologo/agendar_cita.html', {'success':False,
                                                                        'agendar_cita_form':agendar_cita_form()})

        elif 'id_nutriologo' in request.POST:
            #Viene desde la vista del nutriologo
            print('viene desde la vista del nutriologo')

            request.session['id_nutriologo'] = request.POST['id_nutriologo']


            return render(request, 'nutriologo/agendar_cita.html', {'success':True,
                                                                    'agendar_cita_form':agendar_cita_form() })

    elif 'id_nutriologo' in request.session:
        print('refresco la pantalla')
        return render(request, 'nutriologo/agendar_cita.html', {'success':False,
                                                                'agendar_cita_form':agendar_cita_form() })

    print('peticion get normal, pero sin permiso ')
    raise Http404("Estas intentando acceder a una vista sin permiso >:(")




def crear_dieta(request):
    print('crear_dieta')
    print(request)
    if request.method == 'POST':
        print(request.POST)

        if 'carbohidratos' in request.POST:
            print('post del formulario de la cita')
            formulario_dieta = crear_dieta_form(request.POST)

            if formulario_dieta.is_valid():
                print('formulario valido')
                if 'id_paciente' in request.session:
                    id_paciente = request.session['id_paciente']
                    paciente = Usuario.objects.get(id=id_paciente)
                    #creamos la dieta
                    dieta = Dieta.objects.create(nutriologo = request.user,
                                                 paciente = paciente,
                                                 mensaje = formulario_dieta.cleaned_data[''],
                                                 carbohidratos = formulario_dieta.cleaned_data[''],
                                                 azucares = formulario_dieta.cleaned_data[''],
                                                 lipidos = formulario_dieta.cleaned_data[''],
                                                 proteinas = formulario_dieta.cleaned_data[''],
                                                 status = 'vigente',
                                                 )
                    print('se creo sin problemas la cita')
                    return redirect(reverse('usuarios_app:perfil_paciente',kwargs={'username':request.user.username}) )

            else:
                return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                                       'formulario_dieta':crear_dieta_form()})

        elif 'id_paciente' in request.POST:
            #Viene desde la vista del nutriologo
            print('viene desde la vista de nutriologo con el usuario seleccionado')
            request.session['id_paciente'] = request.POST['id_paciente']
            return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                                   'formulario_dieta':crear_dieta_form()})


    elif 'id_paciente' in request.session:
        print('refresco la pantalla')
        return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                               'formulario_dieta':crear_dieta_form()})

    print('peticion get normal, pero sin permiso ')
    raise Http404("Estas intentando acceder a una vista sin permiso >:(")





