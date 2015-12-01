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
from apps.invitados.funciones import cancelarInvitaciones
from apps.metadatos.funciones_metadatos import guardarMetadatos

from apps.notificaciones.funciones import notificacion_bienvenida, notificacion_validar_correo, \
    renka_notificacion_usuario_nuevo
from apps.catalogos.funciones import logger
from apps.proyectos.correos import email_bienvenido, email_validar_usuario
from apps.socios.views import estado_cuenta
from apps.usuarios.funciones import asignar_url_validar_usuario, check_password, crear_relaciones_usuario
from apps.usuarios.models import DocumentoUsuario, RedSocialUser, EstadoCuenta
from .forms import LoginForm, SignUpForm, DesactivarForm, datos_extra_perfil_usuario_form, editarPerfilUsuarioForm, \
    terminar_registro_Form, CuentasForm, DocumentosForm, RedSocialForm
from .models import Usuario, EmailOrUsernameModelBackend, PerfilUsuario, CuentaBancaria




# para enviar mensajes al usuario
from ipware.ip import get_ip
from ipware.ip import get_real_ip
from apps.index.funciones import getPeriodo


def getIP(request):
    ip = get_real_ip(request)
    if ip is not None:
        return ip
    else:
        return get_ip(request)


def login(request):
    # METADATO
    guardarMetadatos(request)
    user_register = SignUpForm()
    login_form = LoginForm()
    template = 'usuarios/login3.html'
    register_error = False

    # print(request.GET)
    url_redireccion = request.GET['next'] if 'next' in request.GET else '/socios/perfil/'

    if request.user.is_authenticated():
        return redirect(url_redireccion)

    if request.method == 'POST':
        # PARA TESTEAR QUE EL USUARIO ACEPTA COOKIES
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        else:
            pass
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
                logger.info("el objeto user es de tipo ")
                logger.info(type(user))
                crear_relaciones_usuario(user, request)
                cancelarInvitaciones(user.email)
                # print('el usuario ahora esta inactivo, pero si pertenece a la pagina ')
                link_usuario = asignar_url_validar_usuario(user)
                # en el email de bienvenida le mandamos el link para confirmar su cuenta

                # email_validar_usuario(request.META['HTTP_HOST'], user, link_usuario,
                #                      asunto='¡ Bienvenido !', destino=[user.email, ])
                # print("se envio correo de validar usuario")
                # notificacion_bienvenida(user)

                # sendEmail(user)
                # #print("Usuario registrado con exito...")
                autentificar = EmailOrUsernameModelBackend()
                user = autentificar.authenticate(
                    username=user_register.cleaned_data['username'].lower().strip().replace(' ', '_'),
                    password=user_register.cleaned_data['password'])
                logger.info("el objeto user(despues de autentificar ) es de tipo ")
                logger.info(type(user))
                try:
                    email_validar_usuario(request.META['HTTP_HOST'], user, link_usuario,
                                          asunto='¡ Bienvenido !', destino=[user.email, ])
                except Exception as e:
                    logger.info('no se pudo mandar correo de bienvenida por ', e)
                notificacion_bienvenida(user)
                renka_notificacion_usuario_nuevo(user, 'loginRenka')
                if user is not None:
                    # if user.is_active:
                    if True:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        return redirect(url_redireccion)
                        # return render(request, template, {'user_register': user_register,
                        #                                  'login_form': login_form,})
                    '''
                    elif not user.is_active:
                        # print('el usuario no ha verificado su cuenta aun')
                        # user.backend = 'django.contrib.auth.backends.ModelBackend'
                        # login(request, user)
                        request.session['cuenta_sin_validar'] = True

                        url_redireccion = '/valida_tu_cuenta'
                        return redirect(url_redireccion)
                    '''
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
                    # #print(user)
                    if user.is_active:
                        user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        return redirect(url_redireccion)
                    else:
                        # user.is_active = True
                        # print('el usuario no ha verificado su cuenta aun')
                        # user.backend = 'django.contrib.auth.backends.ModelBackend'
                        # login(request, user)
                        request.session['cuenta_sin_validar'] = True

                        url_redireccion = '/valida_tu_cuenta'
                        return redirect(url_redireccion)
                        # 'desactivado': 'Gracias por volver a activar tu cuenta !! :D '})

                else:
                    # #print("el usuario y contraseña son invalidos")
                    return render(request, template, {'user_register': user_register,
                                                      'login_form': login_form,
                                                      'error': "El nombre de usuario o contraseña son incorrectos"})
    request.session.set_test_cookie()
    confirmo_correo = False
    try:
        confirmo_correo = request.session['confirmo_correo']
        del request.session['confirmo_correo']
    except Exception as e:
        pass
    return render(request, template, {'user_register': user_register,
                                      'login_form': login_form,
                                      'register_error': register_error,
                                      'url_redireccion': url_redireccion,
                                      'cuentas_form': CuentasForm,
                                      'confirmo_correo': confirmo_correo})


def logOut(request):
    logout(request)
    return redirect('/login')


@login_required
def desactivar_Cuenta(request):
    # METADATO
    guardarMetadatos(request)
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


@login_required
def agregar_redSocial(request):
    # METADATO
    guardarMetadatos(request)
    redes_sociales = RedSocialUser.objects.filter(usuario=request.user)
    if request.is_ajax():
        formRedSocial = RedSocialForm(request.POST)
        if formRedSocial.is_valid():
            try:
                RedSocialUser.objects.create(usuario=request.user, url=formRedSocial.cleaned_data['url'],
                                             tipo_red_social=formRedSocial.cleaned_data['tipo_red_social'])
            except Exception as e:
                logger.exception(e)


@login_required
def editarPerfilUsuario(request):
    # METADATO
    guardarMetadatos(request)
    # new_profile = editarPerfilUsuarioForm(user=request.user)
    new_profile = editarPerfilUsuarioForm()
    perfil = PerfilUsuario.objects.filter(usuario=request.user)[0]
    documentos = DocumentoUsuario.objects.filter(usuario=request.user)
    redes_sociales = RedSocialUser.objects.filter(usuario=request.user)
    cuentas_usuario = CuentaBancaria.objects.filter(usuario=request.user)

    if request.method == 'POST':

        if 'actualizar_perfil' in request.POST:
            profile = PerfilUsuario.objects.get(usuario__pk=request.user.id)
            new_profile = editarPerfilUsuarioForm(request.POST)
            if new_profile.is_valid():
                # usuario = Usuario.objects.filter(id=request.user.id)[0]
                try:
                    actualizarUser(request.user, new_profile)
                except Exception as e:
                    logger.exception(e)
                try:
                    actualizarPerfil(request, profile, new_profile)
                except Exception as e:
                    logger.exception(e)
                try:
                    perfil = PerfilUsuario.objects.get(usuario__pk=request.user.id)
                    return render(request, 'usuarios/editarPerfilUsuario.html', {'new_profile': new_profile,
                                                                                 'cuentas_usuario': cuentas_usuario,
                                                                                 'perfil': perfil,
                                                                                 'documentos': documentos,
                                                                                 'CuentasForm': CuentasForm(),
                                                                                 'DocumentosForm': DocumentosForm(),
                                                                                 'redes_sociales': redes_sociales,
                                                                                 'RedSocialForm': RedSocialForm(),
                                                                                 }, )
                except Exception as e:
                    logger.exception(e)
            else:
                return render(request, 'usuarios/editarPerfilUsuario.html', {'new_profile': new_profile,
                                                                             'cuentas_usuario': cuentas_usuario,
                                                                             'perfil': perfil,
                                                                             'documentos': documentos,
                                                                             'CuentasForm': CuentasForm(),
                                                                             'DocumentosForm': DocumentosForm(),
                                                                             'redes_sociales': redes_sociales,
                                                                             'RedSocialForm': RedSocialForm(),
                                                                             }, )

        if 'sube_documento' in request.POST:
            formDocumentos = DocumentosForm(request.POST)

            if formDocumentos.is_valid():
                try:
                    DocumentoUsuario.objects.create(usuario=request.user, descripcion="",
                                                    archivo="")
                except Exception as e:
                    logger.exception(e)
                documentos = DocumentoUsuario.objects.filter(usuario=request.user)

                return render(request, 'usuarios/editarPerfilUsuario.html', {'new_profile': new_profile,
                                                                             'cuentas_usuario': cuentas_usuario,
                                                                             'perfil': perfil,
                                                                             'documentos': documentos,
                                                                             'CuentasForm': CuentasForm(),
                                                                             'DocumentosForm': DocumentosForm(),
                                                                             'redes_sociales': redes_sociales,
                                                                             'RedSocialForm': RedSocialForm(),
                                                                             }, )

    return render(request, 'usuarios/editarPerfilUsuario.html', {'new_profile': new_profile,
                                                                 'cuentas_usuario': cuentas_usuario,
                                                                 'perfil': perfil,
                                                                 'documentos': documentos,
                                                                 'CuentasForm': CuentasForm(),
                                                                 'DocumentosForm': DocumentosForm(),
                                                                 'redes_sociales': redes_sociales,
                                                                 'RedSocialForm': RedSocialForm(),
                                                                 }, )


@login_required
def perfil_usuario(request):
    # METADATO
    guardarMetadatos(request)
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


def Actualizar_Cuentas(request):
    # METADATO
    guardarMetadatos(request)
    if request.is_ajax():
        POST = request.POST
        perfil_usuario = PerfilUsuario.objects.get(usuario__pk=request.user.id)
        # new_profile = editarPerfilUsuarioForm(request.POST)
        formCuentas = CuentasForm(request.POST)

        if formCuentas.is_valid():
            # print('el form cuenta bancaria fue valido')
            # usuario = Usuario.objects.filter(id=request.user.id)[0]
            try:
                CuentaBancaria.objects.create(usuario=request.user,
                                              titular=formCuentas.cleaned_data['titular'],
                                              sucursal=formCuentas.cleaned_data['sucursal'],
                                              clabe=formCuentas.cleaned_data['clabe'],
                                              banco=formCuentas.cleaned_data['banco'],
                                              numero_de_cuenta=formCuentas.cleaned_data['numero_de_cuenta'])
                # print('se guardo la cuenta bancaria')
            except Exception as e:
                # print(e)
                raise Http404
            return HttpResponse('ok')
        raise Http404
    else:
        raise Http404


class Actualizar_Social_Documentos(TemplateView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        if 'tipo_doc' in request.POST:
            # print("subir documento por ajax")
            # print(request.POST)
            formDocumentos = DocumentosForm(request.POST, request.FILES)
            # print("formDocumentos: ",formDocumentos)
            # print("post ",request.POST)
            # print("files ",request.FILES)
            try:
                DocumentoUsuario.objects.create(usuario=request.user,
                                                descripcion=formDocumentos.cleaned_data['descripcion'],
                                                archivo=request.FILES['archivo'])
                # print("exito al agregar documento ajax")
                documentos = DocumentoUsuario.objects.filter(usuario=request.user)
                documentos = serializers.serialize('json', documentos, fields=('descripcion', 'archivo'))
                return JsonResponse({"documentos": documentos})
            except Exception as e:
                logger.exception(e)
                documentos = RedSocialUser.objects.filter(usuario=request.user)
                documentos = serializers.serialize('json', documentos, fields=('descripcion', 'archivo'))
                return JsonResponse({"documentos": documentos})
                # return HttpResponse(data,mimetype='application/json')
        else:
            pass
            # print(form.Documentos.)
            # print("formulario no valido...")


'''
    <script>
    //form_documentos
        $('#btn-documento').on('click', documentos);
        function documentos()
        {
            $.ajax
            ({
                data: $("#form_documentos").serialize(),
                url: '/editar_ajax/',
                type: 'post',
                success: function (result)
                {
                    result = jQuery.parseJSON(result.documentos);
                    var html=""
                    for (var i=0 ;i<result.length;i++)
                    {
                        //html+= '<span>'+result[i].fields.url+'</span><br><span>'
                        //    +result[i].fields.tipo_red_social+'</span><br>'
                        html+= '<span>Descripcion:' +result[i].fields.descripcion+'</span><br>'
                                +'<span>Documento: ' +result[i].fields.archivo+'</span><br>'
                                +'<span>'+result[i].fields.tipo_doc+'</span><br>'
                    }
                    //console.log(html);
                    $('#div_documentos').html(html);
                },
                error: function (result)
                {
                    alert("No contesta el servidor ");
                }
            });
        }
    </script>
'''


class Eliminar_Cuentas(TemplateView):
    def post(self, request, *args, **kwargs):
        if 'cuenta' in request.POST:
            formCuentas = CuentasForm(request.POST)
            # print("subir cuenta por  ajax")

            if formCuentas.is_valid():
                try:
                    CuentaBancaria.objects.create(usuario=request.user,
                                                  cuenta=formCuentas.cleaned_data['cuenta'],
                                                  descripcion=formCuentas.cleaned_data['descripcion'])

                    # print("exito al agregar cuenta por ajax")
                    cuentas_usuario = CuentaBancaria.objects.filter(usuario=request.user)
                    cuentas_usuario = serializers.serialize('json', cuentas_usuario, fields=('cuenta', 'descripcion'))
                    return JsonResponse({"cuentas_usuario": cuentas_usuario})

                except Exception as e:
                    logger.exception(e)
                    cuentas_usuario = CuentaBancaria.objects.filter(usuario=request.user)
                    cuentas_usuario = serializers.serialize('json', cuentas_usuario, fields=('cuenta', 'descripcion'))
                    return JsonResponse({"cuentas_usuario": cuentas_usuario})


# Necesaria para usuarios por twitter
def terminar_registro(request):
    # validacion de que estamos en el proceso de logueo de twitter
    try:
        backend = request.session['partial_pipeline']['backend']
    except Exception as e:
        logger.exception(e)
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
                    logger.exception(e)
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


# Si el usuario dejo campos en blanco
#   los llenamos con lo que halla puesto antes en nuestra base de datos
def actualizarPerfil(request, perfil, new_profile):
    if new_profile.cleaned_data['imagen']:
        perfil.imagen = new_profile.cleaned_data['imagen']
    if new_profile.cleaned_data['sexo']:
        perfil.sexo = new_profile.cleaned_data['sexo']
    if new_profile.cleaned_data['codigoPostal']:
        perfil.codigoPostal = new_profile.cleaned_data['codigoPostal']
    if new_profile.cleaned_data['pais']:
        perfil.pais = new_profile.cleaned_data['pais']
    if new_profile.cleaned_data['telefono'] != '':
        perfil.telefono = new_profile.cleaned_data['telefono']
    if new_profile.cleaned_data['celular'] != '':
        perfil.celular = new_profile.cleaned_data['celular']
    if new_profile.cleaned_data['fechaNac'] != '':
        perfil.fechaNac = new_profile.cleaned_data['fechaNac']
        hoy = new_profile.cleaned_data['fechaNac']
        lista = str(hoy).replace('-0', '-').split('-')
        hoy = datetime(int(lista[0]), int(lista[1]), int(lista[2]), 10, 0, 0, 0, pytz.UTC).date()
        perfil.fechaNac = hoy
    if not request.FILES:
        pass
    else:
        perfil.imagen = request.FILES['imagen']
    perfil.save()


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
    if desactivar:
        usuario.is_active = False
        # mandamos notificacion de que tiene que validar su correo, y enviar el correo
        email_validar_usuario(path, usuario, asignar_url_validar_usuario(usuario),
                              asunto='Link para activar tu cuenta en RENKA', destino=[usuario.email, ])
        notificacion_bienvenida(usuario)
    usuario.save()


#   Para mostrar el historial de estados de cuenta del empresario
@login_required
def estados_empresario_anteriores(request):
    lista_estados_anteriores = EstadoCuenta.objects.filter(usuario=request.user).exclude(edo_cuenta_empresario='')
    # METADATO
    guardarMetadatos(request)

    return render(request, 'empresarios/historial_estados_empresario.html',
                  {'lista_estados_anteriores': lista_estados_anteriores,
                   'periodo': getPeriodo(),
                   })


def check_user(request):
    #
    # METADATO
    guardarMetadatos(request)
    if request.method == 'GET':
        try:
            # print('metodo get check_user ')

            llave_fin = request.GET['key_user']
            llave_usuario = request.GET['key_secret']
            llave = llave_fin + '_' + llave_usuario

            if not request.user.is_authenticated():
                # print('usuario anonimo')
                try:
                    usuario = get_object_or_404(Usuario, llave_validar_usuario=llave)
                    # des-hasheamos parte del link, para coroborar que si es el hash del usuario
                    # (suponiendo que se repitiera el hash en algun momento)
                    username_hasheado = check_password(usuario.username)
                    # print('usuario.username ',usuario.username)
                    # print('username_hasheado ', username_hasheado )
                    # print( llave_usuario )
                    # print( username_hasheado )
                    if llave_usuario == username_hasheado:
                        # print('el usuario existe, verificamos el username, lo volvemos activo')
                        usuario.is_active = True
                        usuario.llave_validar_usuario = 'valido'
                        usuario.save()
                        notificacion_validar_correo(usuario)
                        # email_bienvenido(request.user, destino=[usuario.email, ])
                        request.session['confirmo_correo'] = True
                        return redirect('/login')
                except Exception as e:
                    logger.exception(e)
                    raise Http404

            if request.user.llave_validar_usuario == 'valido':
                # ya habian habierto el link, y ya se habia validado al usuario
                # print('el usuario ya es valido, respondemos con un mensaje ')
                logger.info('Esta cuenta ya ha sido activada')
                return redirect(reverse('socios_app:perfil'))

            if llave_usuario and llave_fin:
                llave = llave_fin + '_' + llave_usuario
                # print('la llave es ',llave)
                # print('la llave del usuario es ', request.user.llave_validar_usuario)
                if llave == request.user.llave_validar_usuario:
                    # el link es valido
                    # print('el link es valido, lo desactivamos y lo pasamos a activo')
                    request.user.llave_validar_usuario = 'valido'
                    request.user.is_active = True
                    request.user.save()
                    notificacion_validar_correo(request.user)
                    renka_notificacion_usuario_nuevo(request.user, 'loginRenka')
                    # email_bienvenido(request.user, destino=[request.user.email])
                    return redirect(reverse('socios_app:perfil'))

            return render(request, '404.html')
        except Exception as e:
            logger.exception(e)
            raise Http404
    raise Http404


def valida_tu_cuenta(request):
    # METADATO
    guardarMetadatos(request)
    try:
        if request.method == 'POST':
            if 're_enviar' in request.POST:
                # print(request.POST['correo'])
                email = request.POST['correo']
                # validamos que el correo pertenezca a un usuario con una cuenta
                try:
                    usuario = Usuario.objects.get(is_active=False, email=email.lower().strip())
                    # print(usuario)
                    if usuario:
                        if usuario.llave_validar_usuario == 'valido':
                            return render(request, 'usuarios/validar_correo_usuario.html', {'enviado': True,
                                                                                            'error': 'La cuenta ya habia sido validada, puedes iniciar sesion en cualquier momento'})

                        # re enviamos el correo con la informacion
                        email_validar_usuario(request.META['HTTP_HOST'], usuario, asignar_url_validar_usuario(usuario),
                                              asunto='¡ Bienvenido a RENKA !', destino=[usuario.email, ])
                        return render(request, 'usuarios/validar_correo_usuario.html', {'enviado': True, })
                except:
                    return render(request, 'usuarios/validar_correo_usuario.html', {'enviado': False,
                                                                                    'error': 'EL correo que nos proporcionaste no lo tenemos registrado o esta asociado a una cuenta ya validad, por favor revisalo'})

        cuenta_sin_validar = request.session['cuenta_sin_validar']
        del request.session['cuenta_sin_validar']
        return render(request, 'usuarios/validar_correo_usuario.html')
    except:
        return redirect('/login')
