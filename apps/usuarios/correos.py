# -*- encoding: utf-8 -*-
__author__ = 'metallica'
from django.core.mail import EmailMessage
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags, format_html
from django.shortcuts import redirect, render
from django.conf import settings

##      **********************************
##********* CORREO DE BIENVENIDA,

def mailing_bienvenida(usuario, asunto='¡Bienvenido!', destino=['lord.rattlehead@hotmail.com', ]):
    subject = asunto
    from_email = "EDS <carlos.thrashaholic@gmail.com>"
    to = destino
    #print(url_accion)
    ctx = {'usuario': usuario,}
    html_content = render_to_string("correos/correo_bienvenida.html", context=ctx)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        #logger.info("se envio correo de bienvenida")
    except Exception as e:
        #logger.info(e)
        pass


def mailing_cita_agendada_con_exito(usuario, cita, asunto='¡Bienvenido!', destino=['lord.rattlehead@hotmail.com', ]):
    subject = asunto
    from_email = "EDS <carlos.thrashaholic@gmail.com>"
    to = destino
    #print(url_accion)
    ctx = {'usuario': usuario,
           'cita':cita }
    html_content = render_to_string("correos/cita_agendada_con_exito.html", context=ctx)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        #logger.info("se envio correo de bienvenida")
    except Exception as e:
        #logger.info(e)
        pass


def mailing_revisa_tu_dieta(usuario, dieta, asunto='¡Bienvenido!', destino=['lord.rattlehead@hotmail.com', ]):
    subject = asunto
    from_email = "EDS <carlos.thrashaholic@gmail.com>"
    to = destino
    #print(url_accion)
    ctx = {'usuario': usuario,
           'dieta':dieta }
    html_content = render_to_string("correos/revisa_tu_dieta.html", context=ctx)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    try:
        msg.send()
        #logger.info("se envio correo de bienvenida")
    except Exception as e:
        #logger.info(e)
        pass







