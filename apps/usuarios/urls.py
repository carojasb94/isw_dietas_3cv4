__author__ = 'metallica'

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('apps.usuarios.urls', namespace='usuarios_app')),
    url(r'^login/$', 'apps.usuarios.views.log_in', name='login'),
    url(r'^logout$', 'apps.usuarios.views.logOut', name='logout'),

    url(r'^actualizar-a-nutriologo/', 'apps.usuarios.views.actualizar_a_nutriologo', name="actualizar_a_nutriologo"),
    url(r'^solicitud-enviada/', 'apps.usuarios.views.solicitud_enviada', name="solicitud_enviada"),
    url(r'^terminar_registro/', 'apps.usuarios.views.terminar_registro', name="terminar_registro"),
    #url(r'^(?P<username>[\w-]+)/$', 'apps.usuarios.views.perfil_usuario', name='perfil_usuario'),
    url(r'^perfil/(?P<username>[\w-]+)/$', 'apps.usuarios.views.perfil_paciente', name='perfil_paciente'),

]


