from datetime import datetime
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
    lunes_inicio = models.TimeField(null=True,blank=True, default = datetime.now().replace(hour=10, minute=00, second=00) )
    lunes_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    martes_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    martes_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    miercoles_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    miercoles_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    jueves_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    jueves_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    viernes_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    viernes_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    sabado_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    sabado_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))
    domingo_inicio = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=10, minute=00, second=00))
    domingo_fin = models.TimeField(null=True,blank=True, default=datetime.now().replace(hour=16, minute=00, second=00))

    def __str__(self):
        return self.nutriologo

    def __unicode__(self):
        return self.nutriologo


class Cita(models.Model):
    nutriologo = models.ForeignKey(Usuario, related_name='cita_nutriologo')
    paciente = models.ForeignKey(Usuario,related_name='cita_paciente')
    fecha = models.DateTimeField(default=datetime.now())
    mensaje = models.CharField(max_length=100, default='', blank=True)
    status = models.CharField(choices=(('aplicada','aplicada'),('pendiente','pendiente'),('sin_estado','sin_estado')), max_length=30, default="sin_estado")

class Alimento(models.Model):
    nombre = models.CharField(max_length=100, default='', blank=True)

class Dieta(models.Model):
    nutriologo = models.ForeignKey(Usuario, related_name='dieta_nutriologo')
    paciente = models.ForeignKey(Usuario,related_name='dieta_paciente')
    fecha = models.DateTimeField(default=datetime.now())
    mensaje = models.CharField(max_length=100, default='', blank=True)
    status = models.CharField(choices=(('vigente','vigente'),('pasada','pasada')), max_length=30, default="vigente")
    carbohidratos = models.CharField(max_length=50, default="")
    azucares = models.CharField(max_length=50, default="")
    lipidos = models.CharField(max_length=50, default="")
    proteinas = models.CharField(max_length=50, default="")
    #alimento = models.ManyToManyField(Alimento, through='Emprendido', related_name='Empresario')


class HorarioDieta(models.Model):
    dieta = models.ForeignKey(Dieta)
    nutriologo = models.ForeignKey(Usuario, related_name='horarioDieta_nutriologo')
    paciente = models.ForeignKey(Usuario,related_name='horarioDieta_paciente')
    estados = (('lunes', 'lunes'),
               ('martes', 'martes'),
               ('miercoles', 'miercoles'),
               ('jueves', 'jueves'),
               ('viernes', 'viernes'),
               ('sabado', 'sabado'),
               ('domingo', 'domingo'),
               )
    dia = models.CharField(max_length=20, choices=estados, default='lunes')
    fecha = models.DateTimeField(default=datetime.now())










