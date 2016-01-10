# -*- encoding: utf-8 -*-
from django.contrib import admin
from apps.chat.models import Mensaje

@admin.register(Mensaje)
class AdminMensaje(admin.ModelAdmin):
    pass
from django.contrib import admin

# Register your models here.


