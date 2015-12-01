# -*- encoding: utf-8 -*-

from django.contrib import admin
from apps.usuarios.models import Usuario


@admin.register(Usuario)
class AdminUsuario(admin.ModelAdmin):
    pass
