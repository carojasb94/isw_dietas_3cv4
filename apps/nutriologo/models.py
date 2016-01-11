from django.db import models

# Create your models here.
from apps.usuarios.models import Usuario

def cedula_nutriologo_path(instance, filename):
    return "nutriologos/{id}/{file}".format(id=instance.usuario.id, file=filename)


class Medico(models.Model):
    pass


class Consultorio(models.Model):
    nombre = models.CharField(max_length=100)
    numero_consultorio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    medico = models.ForeignKey(Medico)

class Peticion_para_Ser_Nutriologo(models.Model):
    mensaje = models.CharField(max_length=200)
    usuario = models.ForeignKey(Usuario)
    cedula = models.FileField(upload_to=cedula_nutriologo_path, default='')
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return self.mensaje

    def __unicode__(self):
        return self.mensaje

class Horario_de_nutriologo(models.Model):
    nutriologo = models.ForeignKey(Usuario)
    lunes_inicio = models.DateTimeField(null=True,blank=True)
    lunes_fin = models.DateTimeField(null=True,blank=True)
    martes_inicio = models.DateTimeField(null=True,blank=True)
    martes_fin = models.DateTimeField(null=True,blank=True)
    miercoles_inicio = models.DateTimeField(null=True,blank=True)
    miercoles_fin = models.DateTimeField(null=True,blank=True)
    jueves_inicio = models.DateTimeField(null=True,blank=True)
    jueves_fin = models.DateTimeField(null=True,blank=True)
    viernes_inicio = models.DateTimeField(null=True,blank=True)
    viernes_fin = models.DateTimeField(null=True,blank=True)
    sabado_inicio = models.DateTimeField(null=True,blank=True)
    sabado_fin = models.DateTimeField(null=True,blank=True)
    domingo_inicio = models.DateTimeField(null=True,blank=True)
    domingo_fin = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.nutriologo

    def __unicode__(self):
        return self.nutriologo
