__author__ = 'metallica'


class Estructura_Usuario(object):
    username=''
    nombre = ''
    apellidos = ''
    email = ''
    nivel = 'paciente'
    is_nutriologo = False


    def __init__(self,id=0, username='', nombre='', apellidos='' ,email='' ,nivel='', avatar='', is_nutriologo=False):
        self.id=id
        self.username = username
        self.nombre = nombre
        self.apellidos = apellidos
        self.email = email
        self.nivel = nivel
        self.avatar = avatar
        self.is_nutriologo = is_nutriologo



