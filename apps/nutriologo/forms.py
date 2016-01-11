# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from apps.usuarios.models import Usuario
from apps.nutriologo.models import Peticion_para_Ser_Nutriologo

class Actualizar_a_Nutriologo_form(forms.ModelForm):
    '''
    direccion = forms.CharField(max_length=70,
                            widget=forms.TextInput(attrs={
                                'placeholder': 'Direccion',
                                'class': 'form-control',
                                'required': 'false',
                            }))
    '''

    class Meta:
        model = Peticion_para_Ser_Nutriologo
        fields = ('cedula',)

        widgets = {
            'cedula': forms.FileInput(),
        }
        labels = {
            'cedula': _("Cedula profesional o equivalente"),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        print('clean data en form de nutriologo')
        print(cleaned_data)
        #print(cleaned_data['cedula'])
        return cleaned_data


##***********
class Actualizar_Horarios_form(forms.ModelForm):
    class Meta:
        model = Peticion_para_Ser_Nutriologo
        fields = \
            ('lunes_inicio','lunes_fin',
             'martes_inicio','martes_fin',
             'miercoles_inicio','miercoles_fin',
             'jueves_inicio','jueves_fin',
             'viernes_inicio','viernes_fin',
             'sabado_inicio','sabado_fin',
             'domingo_inicio','domingo_fin')

        widgets = {
            'lunes_inicio': forms.DateTimeInput(),
            'lunes_fin': forms.DateTimeInput(),
            'martes_inicio': forms.DateTimeInput(),
            'martes_fin': forms.DateTimeInput(),
            'miercoles_inicio': forms.DateTimeInput(),
            'miercoles_fin': forms.DateTimeInput(),
            'jueves_inicio': forms.DateTimeInput(),
            'jueves_fin': forms.DateTimeInput(),
            'viernes_inicio': forms.DateTimeInput(),
            'viernes_fin': forms.DateTimeInput(),
            'sabado_inicio': forms.DateTimeInput(),
            'sabado_fin': forms.DateTimeInput(),
            'domingo_inicio': forms.DateTimeInput(),
            'domingo_fin': forms.DateTimeInput(),
        }
        labels = {
            'lunes': _("Tu rango de horario libre en Lunes"),
            'martes': _("Tu rango de horario libre en Martes"),
            'miercoles': _("Tu rango de horario libre en Miercoles"),
            'jueves': _("Tu rango de horario libre en Jueves"),
            'viernes': _("Tu rango de horario libre en Viernes"),
            'sabado': _("Tu rango de horario libre en Sabado"),
            'domingo': _("Tu rango de horario libre en Domingo"),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        print('clean data en form de nutriologo')
        print(cleaned_data)
        #print(cleaned_data['cedula'])
        return cleaned_data





