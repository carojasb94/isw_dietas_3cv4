# -*- encoding: utf-8 -*-
from django.http import Http404
from django.conf import settings

from apps.usuarios.models import Usuario

# partial pipeline

from social.pipeline.partial import partial
from django.shortcuts import redirect
from apps.catalogos.models import TipoRedSocial
from django.core.files.base import ContentFile
import json
from requests import request as req, HTTPError

USER_FIELDS = ['username', 'email']


# bajar la imagen de su red social a memoria
def descargar_imagen(backend, strategy, user, response, details, is_new=False, *args, **kwargs):
    # Save Facebook profile photo into a user profile, assuming a profile model
    '''
    print('descargar_imagen')
    print(user)
    print(response)
    print(details)
    print(backend)
    print(strategy)
    print(is_new)
    print(args)
    print(kwargs)
    #'''

    if is_new:
        #print('es nuevo ')
        if backend.name == 'facebook':
            #print('de facebook')
            url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
            try:
                response = req('GET', url, params={'type': 'large'})
                response.raise_for_status()
            except HTTPError as e:
                #print(e)
                pass
            else:
                #perfil_usuario = PerfilUsuario.objects.get(usuario=user)
                #perfil_usuario.imagen.save('{0}_facebook.png'.format(user.username), ContentFile(response.content))
                #perfil_usuario.save()
                #logger.info('imagen facebook descargada usuario nuevo')
                pass

        elif backend.name == 'twitter':
            #print('de twitter')
            #print(response)
            url = response.get('profile_image_url', '').replace('_normal', '')
            #print(url)
            try:
                response = req('GET', url, params={'type': 'large'})
                #print('response')
                #print(response)
                response.raise_for_status()
            except HTTPError as e:
                #print(e)
                pass
            else:
                #perfil_usuario = PerfilUsuario.objects.get(usuario=user)
                #perfil_usuario.imagen.save('{0}_twitter.png'.format(user.username), ContentFile(response.content))
                #perfil_usuario.save()
                #print('imagen twitter descargada usuario nuevo')
                pass
    else:
        #print('es ya usuario viejo ')
        if backend.name is 'facebook':
            #perfil_usuario = PerfilUsuario.objects.get(usuario=user)
            try:
                #dimenciones = perfil_usuario.imagen._get_size()
                #print('si tiene imagen, no se descarga nada')
                return
            except Exception as e :
                #print(e)
                url = 'http://graph.facebook.com/{0}/picture'.format(response['id'])
                try:
                    response = req('GET', url, params={'type': 'large'})
                    response.raise_for_status()
                except HTTPError as e:
                    #print(e)
                    pass
                else:
                    #print('de facebook')
                    #print(response)
                    #perfil_usuario.imagen.save('{0}_facebook.jpg'.format(user.username), ContentFile(response.content))
                    #perfil_usuario.save()
                    #print('imagen facebook descargada usuario viejo')
                    pass
                pass

        elif backend.name is 'twitter':
            #perfil_usuario = PerfilUsuario.objects.get(usuario=user)
            try:
                #dimenciones = perfil_usuario.imagen._get_size()
                #logger.info('si tiene imagen, no se descarga nada')
                return
            except Exception as e:
                url = response.get('profile_image_url', '').replace('_normal', '')
                try:
                    response = req('GET', url, params={'type': 'large'})
                    response.raise_for_status()
                except HTTPError as e:
                    #print(e)
                    pass
                else:
                    #print('de twitter')
                    #print(response)

                    #perfil_usuario.imagen.save('{0}_twitter.png'.format(user.username), ContentFile(response.content))
                    #perfil_usuario.save()
                    #print('imagen twitter descargada usuario viejo')
                    pass
                pass


# Si el usuario existe, lo asociamos, sino pasan
def associate_by_email(**kwargs):
    #print("associate_by_email")
    try:
        email = kwargs['details']['email']
        kwargs['user'] = Usuario.objects.get(email=email)
    except Exception as e:
        #print(e)
        pass
    return kwargs

#   Conseguimos su avatar de fb o twitter
def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    #logger.info("get_avatar")
    url = None
    if backend.name is 'facebook':
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']
    elif backend.name is 'twitter':
        url = response.get('profile_image_url', '').replace('_normal', '')
    if url and (not user.avatar):
        user.avatar = url
        user.save()
    pass

'''
#   El usuario firma los terminos y condiciones
def firma_Termino_y_Condicion(backend, strategy, details, response, user=None, *args, **kwargs):
    if user:
        try:
            FirmaTermYCond.objects.get(usuario=user)
        except Exception as e:
            logger.exception(e)
            FirmaTermYCond.objects.create(
                ususario=user,
                terminoYcondicion=TerminoYCondicion.objects.all().order_by('-fechaCreacion')[0],
                ip="Desconocido"
            )
    else:
        pass
'''
#
def actualizar_datos(usuario, details):
    #logger.info("actualizar_datos")
    if usuario.apellidos == "":
        usuario.apellidos = details['last_name']
        #print('actualizo apellido a %s '%usuario.apellidos)
        usuario.save()
    if usuario.nombre == "":
        usuario.nombre = details['first_name']
        #print('actualizo nombre a %s '%usuario.nombre)
        usuario.save()

#
#
def create_user(strategy, details, user=None, *args, **kwargs):
    '''
    print('create_user')
    print(strategy)
    print(details)
    print(args)
    print(kwargs)
    #'''
    #logger.info("crear usuario social")
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name) or details.get(name))
                  for name in strategy.setting('USER_FIELDS',
                                               USER_FIELDS))
    if not fields:
        return
    #quitamos espacios
    fields['username'] = fields['username'].strip().replace(' ','_').lower()
    try:
        user = Usuario.objects.get(username=fields['username'])
    except Exception as e:
        #logger.info("es usuario nuevo y no existe su username")
        #logger.info(e)
        fields['username'] = fields['username'].strip().replace(' ','_')

        if ((kwargs['backend'].name == 'facebook') or (kwargs['backend'].name == 'linkedin')):
            return {'is_new': True, 'user': strategy.create_user(is_active=True, password=fields['username']+'_'+kwargs['backend'].name, **fields)}
        elif(kwargs['backend'].name == 'twitter'):
            return {'is_new': True, 'user': strategy.create_user(is_active=True, password=fields['username']+'_'+kwargs['backend'].name, **fields)}
        return {'is_new': True, 'user': strategy.create_user(is_active=True, password=fields['username']+'_'+kwargs['backend'].name, **fields)}

    i = 1
    while True:
        try:
            cad = '_00' + str(i)
            user = Usuario.objects.get(username=fields['username'] + cad)
            i += 1
        except:
            fields['username'] = fields['username'] + cad
            fields['username'] = fields['username'].strip().replace(' ','_')
            if ((kwargs['backend'].name == 'facebook') or (kwargs['backend'].name == 'linkedin')):
                return {'is_new': True, 'user': strategy.create_user(is_active=True, password=fields['username']+'_'+kwargs['backend'].name, **fields) }
            elif(kwargs['backend'].name == 'twitter'):
                return {'is_new': True, 'user': strategy.create_user(is_active=True,password=fields['username']+'_'+kwargs['backend'].name,**fields)}
            return {'is_new': True, 'user': strategy.create_user(is_active=True, password=fields['username']+'_'+kwargs['backend'].name, **fields)}

#'''

#
def user_details(strategy, details, user=None, *args, **kwargs):
    """Update user details using data from provider."""
    #logger.info("user_details")
    if kwargs['is_new'] and user:
        actualizar_datos(user, details)
        changed = False  # flag to track changes
        protected = ('username', 'id', 'pk', 'email') + \
                    tuple(strategy.setting('PROTECTED_USER_FIELDS', []))
        for name, value in details.items():
            if not hasattr(user, name):
                continue
            current_value = getattr(user, name, None)
            if not current_value or name not in protected:
                changed |= current_value != value
                setattr(user, name, value)
        if changed:
            strategy.storage.user.changed(user)
    elif user:
        actualizar_datos(user, details)
        #

@partial
def get_email(backend, strategy, request, details, response, user=None, is_new=False, *args, **kwargs):
    '''
    print('estamos en get email ')
    print(backend.name)
    print(strategy)
    print(request)
    print(details)
    print(response)
    print(user)
    print(is_new)
    print(args)
    print(kwargs)
    #'''
    #logger.info("get email")

    if user and user.email:
        return
    elif is_new and backend.name is 'twitter':
        if strategy.session_get('saved_email'):
            try:
                details['email'] = strategy.session_pop('saved_email')
            except Exception as e:
                #logger.exception(e)
                raise Http404('sin mensaje aparentemente')
                # if strategy.session_get('saved_username'):
                #    details['username'] = strategy.session_pop('saved_username')
        else:
            return redirect('/terminar_registro/')

    elif ((is_new) and (backend.name is 'facebook') and (details['email'] == '')):
        #logger.info("se loggeo por fb pero fb no nos mando su correo")
        if strategy.session_get('saved_email'):
            try:
                details['email'] = strategy.session_pop('saved_email')
            except Exception as e:
                #logger.exception(e)
                raise Http404('sin mensaje aparentemente')
        # if strategy.session_get('saved_username'):
        #    details['username'] = strategy.session_pop('saved_username')
        else:
            return redirect('/terminar_registro/')

def robar_informacion(backend, strategy, request, details, response, user=None, is_new=False, *args, **kwargs):
    #logger.info("robar_informacion")
    try:
        return robar_amigos(kwargs['uid'], response['access_token'])
    except Exception as e:
        #print(e)
        return False

def robar_amigos(usuario_uid, access_token):
    url = u'https://graph.facebook.com/{0}/' \
          u'friends?fields=id,name,location,picture' \
          u'&access_token={1}'.format( usuario_uid, access_token,)
    try:
        response = req('GET', url)
        cadena = str(response._content)[2:]
        amigos =  json.loads(cadena[:-1])
        #print(amigos["summary"]["total_count"])
        return amigos["summary"]["total_count"]
    except Exception as e:
        #print(e)
        return False

