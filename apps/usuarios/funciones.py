from apps.nutriologo.models import Cita
from apps.usuarios.estructuras import Estructura_Usuario

__author__ = 'metallica'



def inicializar_estructura_usuario(usuario):
    return Estructura_Usuario(id=usuario.id, username=usuario.username , nombre=usuario.nombre ,
                              apellidos=usuario.apellidos ,email=usuario.email, nivel=usuario.tipo, avatar=usuario.avatar, is_nutriologo=usuario.is_nutriologo)




def tiene_citas_pendientes(usuario):
    print('tiene_citas pendientes')
    citas = Cita.objects.filter(paciente=usuario).filter(status='pendiente').exclude(status='sin_estado')
    return citas

def tiene_citas_pasadas(usuario):
    print('tiene_citas aplicadas')
    citas = Cita.objects.filter(paciente=usuario).filter(status='aplicada').exclude(status='sin_estado')
    return citas


def tiene_citas_pendientes_nutriologo(usuario):
    print('tiene_citas aplicadas nutriologo')
    citas = Cita.objects.filter(nutriologo=usuario).filter(status='aplicada').exclude(status='sin_estado')
    return citas


