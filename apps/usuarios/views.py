# -*- encoding: utf-8 -*-
from datetime import datetime

from django.core.urlresolvers import reverse
from django.http import JsonResponse, HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core import serializers

import pytz
from apps.nutriologo.forms import Actualizar_a_Nutriologo_form
from apps.nutriologo.models import Peticion_para_Ser_Nutriologo
from apps.usuarios.constantes import mensaje_nutriologo
from apps.usuarios.funciones import inicializar_estructura_usuario

from .forms import LoginForm, SignUpForm, DesactivarForm, terminar_registro_Form

from .models import Usuario, EmailOrUsernameModelBackend


def log_in(request):
    user_register = SignUpForm()
    login_form = LoginForm()
    template = 'usuarios/login3.html'
    register_error = False

    url_redireccion = request.GET['next'] if 'next' in request.GET else '/'

    if request.user.is_authenticated():
        print('usuario ya autenticado')
        return redirect(url_redireccion)

    if request.method == 'POST':
        # PARA TESTEAR QUE EL USUARIO ACEPTA COOKIES
        if 'register_form' in request.POST:
            user_register = SignUpForm(request.POST)
            if user_register.is_valid():
                #   CREAMOS EL USUARIO
                user = Usuario.objects.create_user(
                    username=user_register.cleaned_data['username'].lower().strip().replace(' ', '_'),
                    email=user_register.cleaned_data['email'].lower(),
                    password=user_register.cleaned_data['password'],
                    is_active=True)
                #   CREAMOS LOS OBJETOS QUE SE RELACIONAN CON EL
                # print('el usuario ahora esta inactivo, pero si pertenece a la pagina ')
                autentificar = EmailOrUsernameModelBackend()
                user = autentificar.authenticate(
                    username=user_register.cleaned_data['username'].lower().strip().replace(' ', '_'),
                    password=user_register.cleaned_data['password'])
                if user is not None:
                    # if user.is_active:
                    if True:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        if url_redireccion == '/':
                            url_redireccion = reverse('usuarios_app:perfil_paciente', kwargs={'username':user.username})
                        return redirect(url_redireccion)
                        # return render(request, template, {'user_register': user_register,
                        #                                  'login_form': login_form,})
            register_error = True

        if 'login_form' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                autentificar = EmailOrUsernameModelBackend()
                user = autentificar.authenticate(
                    username=login_form.cleaned_data['username'].lower().strip().replace(' ', '_'),
                    password=login_form.cleaned_data['password'])
                # #print(user)
                if user is not None:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, user)
                    if url_redireccion == '/':
                        url_redireccion = reverse('usuarios_app:perfil_paciente', kwargs={'username':user.username})
                    return redirect(url_redireccion)

                else:
                    # #print("el usuario y contraseña son invalidos")
                    return render(request, template, {'user_register': user_register,
                                                      'login_form': login_form,
                                                      'error': "El nombre de usuario o contraseña son incorrectos"})

    return render(request, template, {'user_register': user_register,
                                      'login_form': login_form,
                                      'register_error': register_error,
                                      'url_redireccion': url_redireccion, })


def logOut(request):
    logout(request)
    return redirect('/login')


@login_required
def desactivar_Cuenta(request):
    # METADATO
    if request.POST:
        # #print("entramos a desactivarForm..")
        form = DesactivarForm(request.POST)
        if form.is_valid():

            request.user.is_active = False
            request.user.save()
            logout(request)
            return redirect('/')
        else:
            return render(request, "usuarios/desactivar_Cuenta.html",
                          {"form": form, 'error': ''})
    else:
        form = DesactivarForm()

    return render(request, "usuarios/desactivar_Cuenta.html", {"form": form})




# Necesaria para usuarios por twitter
def terminar_registro(request):
    # validacion de que estamos en el proceso de logueo de twitter
    try:
        backend = request.session['partial_pipeline']['backend']
    except Exception as e:
        #logger.exception(e)
        return render(request, '404.html')

    if request.method == "POST":
        if 'email' in request.POST:
            form = terminar_registro_Form(request.POST)
            if form.is_valid():
                request.session['saved_email'] = request.POST['email']
                # if 'username' in request.POST:
                # request.session['saved_username'] = request.POST['username']
                try:
                    backend = request.session['partial_pipeline']['backend']
                    url = '/complete/%s/' % backend
                    return redirect(url)
                except Exception as e:
                    #logger.exception(e)
                    return render(request, '404.html')
            return render(request, 'usuarios/get_email.html', {'form': form})
    red_social = 1
    # print(request)
    return render(request, 'usuarios/get_email.html', {'form': terminar_registro_Form()})



def perfil_usuario(request, username):
    print(username)
    if request.user.is_authenticated():
        print("usuario loggeado")
        print(request.user.username)
        if username == request.user.username:
            print("es propietario del perfil")

        return render(request, 'usuarios/vista_usuario__.html',{'mi_perfil':True})
    else:
        return render(request, 'usuarios/vista_usuario__.html',{'mi_perfil':False})

    raise Http404("Ocurrio un error, vuelva a intentarlo")


# perfil_paciente
def perfil_paciente(request, username):
    print('perfil paciente')
    print(username)
    #try:
    if True:
        usuario = Usuario.objects.get(username=username)
        if request.user.is_authenticated():
            print("usuario loggeado")
            print(request.user.username)
            if username == request.user.username:
                print("es propietario del perfil")

                return render(request, 'usuarios/perfil_paciente.html',{'anonimo' : False,
                                                                        'mi_perfil' : True,
                                                                        'usuario': inicializar_estructura_usuario(request.user),
                                                                    })
            #sacamos de la base de datos la demas informacion del ysyarui al que kle estan visitando su perfil
            return render(request, 'usuarios/perfil_paciente.html',{'anonimo' : False,
                                                                    'mi_perfil' : False,
                                                                    'usuario' : inicializar_estructura_usuario(usuario),
                                                                    })
        else:
            return render(request, 'usuarios/perfil_paciente.html',{'anonimo':True,
                                                                    'usuario' : inicializar_estructura_usuario(usuario),
                                                                    })
    #except Exception as e:
    #    raise Http404("No existe ese nombre de usuario D= : "+str(e),' '+str(e.args))



# actualizar_a_nutriologo
@login_required
def actualizar_a_nutriologo(request):
    try:
        if request.method == 'POST':
            print('metodo post actualizar_a_nutriologo')
            print(request.POST)
            print(request.FILES)
            actualizar_a_nutriologo_form = Actualizar_a_Nutriologo_form(request.POST, request.FILES)
            print(actualizar_a_nutriologo_form)

            if actualizar_a_nutriologo_form.is_valid():
                print('form valido')
                Peticion_para_Ser_Nutriologo(mensaje = mensaje_nutriologo%(request.user.username),
                                             usuario = request.user,
                                             cedula = request.FILES['cedula'],
                                             )
                actualizar_a_nutriologo_form.save()
                return redirect(reverse('usuarios_app:solicitud_enviada'))
            else:
                print('form no valido')
            return render(request, 'usuarios/actualizar_a_nutriologo.html',{'nutriologo_form':Actualizar_a_Nutriologo_form(),
                                                                            'error':True})

        return render(request, 'usuarios/actualizar_a_nutriologo.html',{'nutriologo_form':Actualizar_a_Nutriologo_form() })

    except Exception as e:
        raise Http404("Ocurrio un error, vuelva a intentarlo "+str(e)+' '+str(e.args))


def solicitud_enviada(request):
    print('solicitud_enviada')
    return render(request, 'usuarios/solicitud_enviada.html',{})


'''
@login_required
def perfil_usuario(request):
    # METADATO
    perfil = PerfilUsuario.objects.get(usuario=request.user)

    new_profile = editarPerfilUsuarioForm(instance=perfil)
    documentos = DocumentoUsuario.objects.filter(usuario=request.user)
    cuentas_bancarias = CuentaBancaria.objects.filter(usuario=request.user)

    # cuentas_usuario = CuentaBancaria.objects.filter(usuario=request.user)
    errores = []
    if request.method == 'POST':
        if 'actualizar_perfil' in request.POST:
            profile = PerfilUsuario.objects.get(usuario__pk=request.user.id)
            new_profile = editarPerfilUsuarioForm(request.POST)
            if new_profile.is_valid():
                # usuario = Usuario.objects.filter(id=request.user.id)[0]
                email = new_profile.cleaned_data['email']
                if ((email != '') and (email != request.user.email)):
                    # verificamos que el correo al que se va a cambiar sea valido
                    try:
                        # print('el usuario quiere cambiar el correo')
                        Usuario.objects.get(email=email)
                        errores.append('Ese mail ya esta en uso')
                        new_profile.add_error('email', 'Ese mail ya esta en uso...')
                        # print('el email existe')
                        new_profile.cleaned_data['email'] = request.user.email
                        # print(new_profile.cleaned_data['email'])
                        try:
                            actualizarUser(request.user, new_profile)
                        except Exception as e:
                            logger.exception(e)
                        try:
                            actualizarPerfil(request, profile, new_profile)
                        except Exception as e:
                            logger.exception(e)

                        perfil = PerfilUsuario.objects.get(usuario__pk=request.user.id)
                        return render(request, 'usuarios/perfil_usuario.html', {'new_profile': new_profile,
                                                                                # 'cuentas_usuario': cuentas_usuario,
                                                                                'perfil': perfil,
                                                                                'documentos': documentos,
                                                                                # 'CuentasForm': CuentasForm(),
                                                                                'DocumentosForm': DocumentosForm(),
                                                                                'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                                                'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                                                'errores': errores,
                                                                                }, )
                    except Exception as e:
                        logger.info(e)
                        # print(new_profile.cleaned_data['email'])

                        try:
                            # se 'desactiva' su cuenta, hasta que valide su nuevo correo
                            # DESACTIVA CORREO NOTIFICACION al usuario dentro de actualizarUser
                            actualizarUser(request.user, new_profile, desactivar=True, path=request.META['HTTP_HOST'])
                        except Exception as e:
                            logger.exception(e)
                        try:
                            actualizarPerfil(request, profile, new_profile)
                        except Exception as e:
                            logger.exception(e)

                        perfil = PerfilUsuario.objects.get(usuario__pk=request.user.id)
                        return render(request, 'usuarios/perfil_usuario.html', {'new_profile': new_profile,
                                                                                'perfil': perfil,
                                                                                'documentos': documentos,
                                                                                'DocumentosForm': DocumentosForm(),
                                                                                'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                                                'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                                                }, )
                elif (email == request.user.email):
                    # caso normal, en el que no cambia su correo
                    # print(new_profile.cleaned_data['email'])
                    try:
                        actualizarUser(request.user, new_profile)
                    except Exception as e:
                        logger.exception(e)
                    try:
                        actualizarPerfil(request, profile, new_profile)
                    except Exception as e:
                        logger.exception(e)
                    perfil = PerfilUsuario.objects.get(usuario__pk=request.user.id)
                    return render(request, 'usuarios/perfil_usuario.html', {'new_profile': new_profile,
                                                                            'perfil': perfil,
                                                                            'documentos': documentos,
                                                                            'DocumentosForm': DocumentosForm(),
                                                                            'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                                            'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                                            }, )

            else:
                return render(request, 'usuarios/perfil_usuario.html', {'new_profile': new_profile,
                                                                        # 'cuentas_usuario': cuentas_usuario,
                                                                        'perfil': perfil,
                                                                        'documentos': documentos,
                                                                        # 'CuentasForm': CuentasForm(),
                                                                        'DocumentosForm': DocumentosForm(),
                                                                        'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                                        'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                                        }, )

        if 'sube_documento' in request.POST:
            formDocumentos = DocumentosForm(request.POST)

            if formDocumentos.is_valid():
                try:
                    DocumentoUsuario.objects.create(usuario=request.user, descripcion="",
                                                    archivo="", )
                except Exception as e:
                    logger.exception(e)
                documentos = DocumentoUsuario.objects.filter(usuario=request.user)

                return render(request, 'usuarios/editarPerfilUsuario.html', {'new_profile': new_profile,
                                                                             # 'cuentas_usuario': cuentas_usuario,
                                                                             'perfil': perfil,
                                                                             'documentos': documentos,
                                                                             # 'CuentasForm': CuentasForm(),
                                                                             'DocumentosForm': DocumentosForm(),
                                                                             'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                                             'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                                             }, )

    return render(request, 'usuarios/perfil_usuario.html', {'perfil': perfil,
                                                            'new_profile': new_profile,
                                                            'DocumentosForm': DocumentosForm(),
                                                            'fecha_nacimiento': perfil.fechaNac.isoformat(),
                                                            'datos_extra_form': datos_extra_perfil_usuario_form(),
                                                            'cuentas_form': CuentasForm(),
                                                            'cuentas_bancarias': cuentas_bancarias,
                                                            })
'''


'''
@csrf_exempt
def ajax_datos_extra(request):
    # METADATO
    guardarMetadatos(request)
    if request.is_ajax():
        POST = request.POST
        # print(POST)
        perfil_usuario = PerfilUsuario.objects.get(usuario__pk=request.user.id)
        # new_profile = editarPerfilUsuarioForm(request.POST)
        datos_extra = datos_extra_perfil_usuario_form(request.POST, request.FILES, instance=perfil_usuario)
        if datos_extra.is_valid():
            # print('el form new_profile fue valido')
            # usuario = Usuario.objects.filter(id=request.user.id)[0]
            try:
                datos_extra.save()
                # actualizar_datos_extra(datos_extra)
            except Exception as e:
                # print(e)
                pass
            return HttpResponse('ok')
        raise Http404
    else:
        raise Http404
'''


# Necesaria para usuarios por twitter
def terminar_registro(request):
    # validacion de que estamos en el proceso de logueo de twitter
    try:
        backend = request.session['partial_pipeline']['backend']
    except Exception as e:
        return render(request, '404.html')
        pass

    if request.method == "POST":
        if 'email' in request.POST:
            form = terminar_registro_Form(request.POST)
            if form.is_valid():
                request.session['saved_email'] = request.POST['email']
                # if 'username' in request.POST:
                # request.session['saved_username'] = request.POST['username']
                try:
                    backend = request.session['partial_pipeline']['backend']
                    url = '/complete/%s/' % backend
                    return redirect(url)
                except Exception as e:
                    #logger.exception(e)
                    return render(request, '404.html')
            return render(request, 'usuarios/get_email.html', {'form': form})
    red_social = 1
    # print(request)
    return render(request, 'usuarios/get_email.html', {'form': terminar_registro_Form()})


def validar_email_twitter(email):
    if (email == ''):
        mensaje = "Necesitamos una cuenta de correo para poder crea tu cuenta"
        return False, mensaje
    else:
        try:
            usuario = Usuario.objects.get(email=email)
            mensaje = "Ya existe un usuario con ese email, disculpa"
            # print(usuario)
            return False, mensaje
        except Exception as e:
            return True, ''


#   Si el usuario dejo campos en blanco
#   los llenamos con lo que halla puesto antes en nuestra base de datos
def actualizarUser(usuario, new_profile, desactivar=False, path='http://www.somosrenka.com'):
    if new_profile.cleaned_data['nombre']:
        usuario.nombre = new_profile.cleaned_data['nombre']
    if new_profile.cleaned_data['apellidos']:
        usuario.apellidos = new_profile.cleaned_data['apellidos']
    if new_profile.cleaned_data['email']:
        usuario.email = new_profile.cleaned_data['email']
    if new_profile.cleaned_data['anonimo'] != '':
        usuario.anonimo = new_profile.cleaned_data['anonimo']
        print('anonimo', usuario.anonimo)
    usuario.save()
