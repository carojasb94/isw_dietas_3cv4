from apps.usuarios.estructuras import Estructura_Usuario

__author__ = 'metallica'



def inicializar_estructura_usuario(usuario):
    return Estructura_Usuario(id=usuario.id, username=usuario.username , nombre=usuario.nombre ,
                              apellidos=usuario.apellidos ,email=usuario.email, nivel=usuario.tipo, avatar=usuario.avatar, is_nutriologo=usuario.is_nutriologo)

