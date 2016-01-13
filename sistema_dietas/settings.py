# -*- encoding: utf-8 -*-

from .base import *
import pymysql

pymysql.install_as_MySQLdb()

#'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'thrashformer$db_eds',
        'HOST': 'thrashformer.mysql.pythonanywhere-services.com',
        'USER': 'thrashformer',
        'PASSWORD': 'elnanoz1!',
        'PORT': '3306',
    }
}
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_karussa.sqlite3'),
    }
}

#'''


NOMBRE_LOG = "local"
DIRECCION_BASE = 'http://localhost:8000/'

DEBUG = True


#########   SETTINGS DE SWAMPDRAGON ##################
# Indispensable
#   Esta configuracion aplica si swampdragon no usa algun sistema de autenticacion o cosas asi
# SWAMP_DRAGON_CONNECTION = ('swampdragon.connections.sockjs_connection.DjangoSubscriberConnection', '/data')
# Esta configuracion ya trae implementado un modelo de usuario para swampdragon
SWAMP_DRAGON_CONNECTION = ('swampdragon_auth.socketconnection.HttpDataConnection', '/data')
'''
DRAGON_URL = 'http://localhost:9999/'
#http://192.168.2.8:8001/
'''
# escuchando en localhost
SWAMP_DRAGON_HOST = 'localhost'
# puerto de escucha
SWAMP_DRAGON_PORT = '9999'  # default '9999'
# url en la que va estar escuchando para recibir mensajes y esas cosas

DRAGON_URL = 'http://localhost:9999/'



