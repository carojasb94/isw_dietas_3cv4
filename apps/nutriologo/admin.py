# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.nutriologo.models import Consultorio, Peticion_para_Ser_Nutriologo

@admin.register(Consultorio)
class AdminConsultorio(admin.ModelAdmin):
    pass

@admin.register(Peticion_para_Ser_Nutriologo)
class AdminPeticiones(admin.ModelAdmin):
    pass


