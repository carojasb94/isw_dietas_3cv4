# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.nutriologo.models import Consultorio, Peticion_para_Ser_Nutriologo, Horario_de_nutriologo


@admin.register(Consultorio)
class AdminConsultorio(admin.ModelAdmin):
    pass


def aprobar_solicitud(self, request, queryset):
    for q in queryset:
        print(self)
        print(queryset)
        #Actualizamos el status de la peticion
        q.aprobado = True
        usuario = q.usuario
        #Buscamos al usuario para pasarlo a ser nutriologo
        Horario_de_nutriologo.objects.get_or_create(nutriologo=usuario)
        usuario.is_nutriologo = True
        usuario.termino_horarios = True
        usuario.save()
        q.save()
    return queryset

@admin.register(Peticion_para_Ser_Nutriologo)
class AdminPeticiones(admin.ModelAdmin):
    actions = [aprobar_solicitud, ]

    pass

@admin.register(Horario_de_nutriologo)
class AdminHorariosNutriologo(admin.ModelAdmin):
    pass



