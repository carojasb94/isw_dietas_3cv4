__author__ = 'metallica'

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^', include('apps.usuarios.urls', namespace='usuarios_app')), home
    url(r'^$', 'apps.home.views.home', name='home'),
    url(r'^equipo/$', 'apps.home.views.equipo', name='equipo'),

]
