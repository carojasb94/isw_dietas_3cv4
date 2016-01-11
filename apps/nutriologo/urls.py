
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^agendar_cita/$', 'apps.nutriologo.views.agendar_cita', name='agendar_cita'),
    url(r'^crear_dieta/$', 'apps.nutriologo.views.crear_dieta', name='crear_dieta'),


]



