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
                                                 mensaje = formulario_dieta.cleaned_data['mensaje'],
                                                 carbohidratos = formulario_dieta.cleaned_data['carbohidratos'],
                                                 azucares = formulario_dieta.cleaned_data['azucares'],
                                                 lipidos = formulario_dieta.cleaned_data['lipidos'],
                                                 proteinas = formulario_dieta.cleaned_data['proteinas'],
                                                 status = 'vigente',
                                                 )

                    print('se creo sin problemas la cita')
                    #volvemos pasadas todas las dietas que esten hasta el momento
                    dietas_anteriores = Dieta.objects.all().exclude(id=dieta.id).exclude(status='pasada')
                    for dieta in dietas_anteriores:
                        dieta.status='pasada'
                        dieta.save()

                    # AHORA SE CANCELA O PASA A 'PASADA' LA CITA
                    if 'id_cita' in request.session:
                        id_paciente = request.session['id_cita']
                        citas = Cita.objects.filter(nutriologo = request.user,
                                                   paciente = paciente, id=id_cita)
                        for cita in citas:
                            cita.status='aplicada'
                            cita.save()
                        del request.session['id_paciente']
                        del request.session['id_cita']


                    return redirect(reverse('usuarios_app:perfil_paciente',kwargs={'username':request.user.username}) )

            else:
                return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                                       'formulario_dieta':crear_dieta_form()})

        elif 'id_paciente' in request.POST and 'id_cita' in request.POST:
            #Viene desde la vista del nutriologo
            print('viene desde la vista de nutriologo con el usuario seleccionado')
            request.session['id_paciente'] = request.POST['id_paciente']
            request.session['id_cita'] = request.POST['id_cita']
            return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                                   'formulario_dieta':crear_dieta_form()})


    elif 'id_paciente' in request.session:
        print('refresco la pantalla')
        return render(request, 'nutriologo/crear_dieta.html', {'success':False,
                                                               'formulario_dieta':crear_dieta_form()})

    print('peticion get normal, pero sin permiso ')
    raise Http404("Estas intentando acceder a una vista sin permiso >:(")


def mis_dietas(request):
    print('mis_dietas')
    print (request)

    dietas_pasadas = dame_dietas_pasadas(usuario)
    dieta_vigente = dame_dieta_vigente(usuario)
    return render(request, 'nutriologo/mis_dietas.html', {'dietas_pasadas':dietas_pasadas,
                                                          'dieta_vigente':dieta_vigente, })



