# -*- encoding: utf-8 -*-

from .base import *
import pymysql

pymysql.install_as_MySQLdb()

'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_karussa',
        'HOST': '162.243.186.32',
        'USER': 'dev',
        'PASSWORD': 'Rd3nvK$',
        'PORT': '3306',
    },
    'db_videos': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test_videos',
        'HOST': '162.243.186.32',
        'USER': 'dev',
        'PASSWORD': 'Rd3nvK$',
        'PORT': '3306',
    }
}
#'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_karussa.sqlite3'),
    }
}

NOMBRE_LOG = "local"
DIRECCION_BASE = 'http://localhost:8000/'

DEBUG = True


