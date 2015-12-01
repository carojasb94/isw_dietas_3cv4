# -*- encoding: utf-8 -*-
__author__ = 'metallica'

from django.shortcuts import redirect
from social.apps.django_app.middleware import SocialAuthExceptionMiddleware
from social.exceptions import *

class CustomSocialAuthExceptionMiddleware(SocialAuthExceptionMiddleware):
    def process_exception(self, request, exception):
        # StopPipeline, dentro del arreglo de excepciones
        if type(exception) in [AuthFailed, AuthCanceled, AuthUnknownError,
                               AuthTokenError, AuthMissingParameter,
                               AuthAlreadyAssociated,
                               WrongBackend, NotAllowedToDisconnect,
                               AuthStateMissing, AuthStateForbidden, AuthTokenRevoked]:
            #print ('excepcion : ',exception)
            #logger.info('si ocurren cosas raras, estoy en metadatos/middlewares y estoy cachando alguna excepcion de mas que no es social')
            return redirect('/login')
        else:
            pass
