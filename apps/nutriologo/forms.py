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








