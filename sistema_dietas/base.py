# -*- encoding: utf-8 -*-

import sys
from datetime import datetime

import os
import pytz
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from unipath import Path

SECRET_KEY = 'z10e=pxmx$ic!2%3w90uv(gk-*0%-h6nu-wom0s3nia-h6gc91'

USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGE_CODE = 'es-MX'

DEFAULT_CHARSET = 'utf-8'
FILE_CHARSET = 'utf-8'

TIME_ZONE = 'America/Mexico_City'

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    # 'material.frontend.context_processors.modules',
    # 'apps.metadatos.middlewares.get_current_path',

)

BASE_DIR = Path(__file__).ancestor(2)
print(BASE_DIR)

LOGIN_URL = '/login/'

ALLOWED_HOSTS = ['*', ]

ADMINS = (('Carlos_Alberto', 'lord.rattlehead@hotmail.com'),)

MANAGERS = (('Carlos_Alberto', 'lord.rattlehead@hotmail.com'),)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
)

LOCAL_APPS = (
    'apps.usuarios',
    'apps.dieta',
    'apps.home',

)

THIRD_PARTY_APPS = (
    'suit',
    'social.apps.django_app.default',
)

FIXTURE_DIRS = (
    '/datos_base/',
)

INSTALLED_APPS = THIRD_PARTY_APPS + DJANGO_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.middleware.security.SecurityMiddleware',
    # 'django_user_agents.middleware.UserAgentMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'sistema_dietas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

#print(TEMPLATES[0]['DIRS'])

WSGI_APPLICATION = 'sistema_dietas.wsgi.application'

STATIC_ROOT = '/static/'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# **************    CONFIGURACION DE CORREOS
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'carlos.thrashaholic@gmail.com'
EMAIL_HOST_PASSWORD = 'Thrashaholic1\"'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'carlos.thrashaholic@gmail.com'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AUTH_USER_MODEL = 'usuarios.Usuario'


NOMBRE_LOG = "local"

def formato_fecha(fecha):
    hoy = datetime(fecha.year, fecha.month, fecha.day, 12, 0, 0, 0, pytz.UTC)
    return hoy.strftime('%Y-%m-%d')

#########   CONFIGURACIONES PARA LOGIN SOCIAL


SOCIAL_AUTH_FACEBOOK_KEY = '793051900816959'  #
SOCIAL_AUTH_FACEBOOK_SECRET = '35b4863123bd7291646edd94d0f390f1'  #

# para obtener permisos extra de facebook, obtenemos el email
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_friends']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}



# redireccion cuando el usuario se logre logear
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/paciente/perfil'
SOCIAL_AUTH_LOGIN_URL = '/paciente/perfil'
SOCIAL_AUTH_USER_MODEL = 'usuarios.Usuario'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'apps.usuarios.pipelineCustom.get_email',
    'apps.usuarios.pipelineCustom.associate_by_email',
    # 'social.pipeline.user.create_user',
    'apps.usuarios.pipelineCustom.create_user',
    'social.pipeline.user.get_username',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'apps.usuarios.pipelineCustom.user_details',
    'apps.usuarios.pipelineCustom.get_avatar',
    'apps.usuarios.pipelineCustom.verificarRed',
    'apps.usuarios.pipelineCustom.descargar_imagen',
    'apps.usuarios.pipelineCustom.crear_relaciones_usuario_social',
    # 'apps.usuarios.pipelineCustom.firma_Termino_y_Condicion',
    # 'apps.usuarios.pipelineCustom.robar_informacion',
)


