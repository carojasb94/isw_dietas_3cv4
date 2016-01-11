# -*- encoding: utf-8 -*-
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from apps.usuarios.models import Usuario
from apps.nutriologo.models import Peticion_para_Ser_Nutriologo, Horario_de_nutriologo, Cita
from datetimewidget.widgets import DateTimeWidget

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
        model = Horario_de_nutriologo
        fields = \
            ('lunes_inicio','lunes_fin',
             'martes_inicio','martes_fin',
             'miercoles_inicio','miercoles_fin',
             'jueves_inicio','jueves_fin',
             'viernes_inicio','viernes_fin',
             'sabado_inicio','sabado_fin',
             'domingo_inicio','domingo_fin')

        widgets = {
            'lunes_inicio': forms.TimeInput(format='%H:%M'),
            'lunes_fin': forms.TimeInput(format='%H:%M'),
            'martes_inicio': forms.TimeInput(format='%H:%M'),
            'martes_fin': forms.TimeInput(format='%H:%M'),
            'miercoles_inicio': forms.TimeInput(format='%H:%M'),
            'miercoles_fin': forms.TimeInput(format='%H:%M'),
            'jueves_inicio': forms.TimeInput(format='%H:%M'),
            'jueves_fin': forms.TimeInput(format='%H:%M'),
            'viernes_inicio': forms.TimeInput(format='%H:%M'),
            'viernes_fin': forms.TimeInput(format='%H:%M'),
            'sabado_inicio': forms.TimeInput(format='%H:%M'),
            'sabado_fin': forms.TimeInput(format='%H:%M'),
            'domingo_inicio': forms.TimeInput(format='%H:%M'),
            'domingo_fin': forms.TimeInput(format='%H:%M'),
        }
        labels = {
            'lunes_inicio': _("Desde"),
            'lunes_fin': _("Hasta"),
            'martes_inicio': _("Desde"),
            'martes_fin': _("Hasta"),
            'miercoles_inicio': _("Desde"),
            'miercoles_fin': _("Hasta"),
            'jueves_inicio': _("Desde"),
            'jueves_fin': _("Hasta"),
            'viernes_inicio': _("Desde"),
            'viernes_fin': _("Hasta"),
            'sabado_inicio': _("Desde"),
            'sabado_fin': _("Hasta"),
            'domingo_inicio': _("Desde"),
            'domingo_fin': _("Hasta"),
        }

    def clean(self):
        cleaned_data = self.cleaned_data
        print('clean data en form de nutriologo')
        print(cleaned_data)
        #print(cleaned_data['cedula'])
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(Actualizar_Horarios_form, self).__init__(*args, **kwargs)



class agendar_cita_form(forms.ModelForm):
    class Meta:
        model = Cita

        fields = ('fecha','mensaje',)

        widgets = {'fecha': forms.DateTimeInput(),
                   'mensaje':forms.Textarea(),
                   }

        labels = {'fecha': _("El dia y hora que desarias fuera tu cita"),
                  'mensaje':_("Algun comentario extra que quieras enviarle al nutriologo ")
                  }



    def clean(self):
        cleaned_data = self.cleaned_data
        print('clean data en form de nutriologo')
        print(cleaned_data)
        #print(cleaned_data['cedula'])
        return cleaned_data
