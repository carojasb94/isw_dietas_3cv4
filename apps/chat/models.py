from datetime import datetime
from django.db import models
from apps.usuarios.models import Usuario

# Create your models here.


class Mensaje(models.Model):
    remitente = models.ForeignKey(Usuario, related_name='UsuarioRemitente')
    destinatario = models.ForeignKey(Usuario,related_name='UsuarioDestinatario')
    mensaje = models.CharField(max_length=100, default='', blank=True)
    fecha = models.DateTimeField(default=datetime.now())















