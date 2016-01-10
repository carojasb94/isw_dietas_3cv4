# -*- encoding: utf-8 -*-
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from apps.dieta.models import Dieta

@admin.register(Dieta)
class AdminDieta(admin.ModelAdmin):
    pass
