# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_usuario_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(default=b'paciente', max_length=30, choices=[(b'nutriologo', b'nutriologo'), (b'paciente', b'paciente'), (b'inactivo', b'inactivo')]),
        ),
    ]
