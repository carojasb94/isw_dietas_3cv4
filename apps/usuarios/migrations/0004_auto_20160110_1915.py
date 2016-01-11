# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_auto_20160107_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='codigo_postal',
            field=models.CharField(default=b'00000', max_length=30),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fecha_nacimiento',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 15, 14, 372087)),
        ),
        migrations.AddField(
            model_name='usuario',
            name='sexo',
            field=models.CharField(default=b'N/A', max_length=30, choices=[(b'Hombre', b'Hombre'), (b'Mujer', b'Mujer'), (b'N/A', b'N/A')]),
        ),
        migrations.AddField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(default=b'xx-xxxxxxxx', max_length=30),
        ),
        migrations.AddField(
            model_name='usuario',
            name='termino_horarios',
            field=models.BooleanField(default=False),
        ),
    ]
