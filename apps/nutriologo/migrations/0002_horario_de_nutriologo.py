# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nutriologo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario_de_nutriologo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lunes_inicio', models.DateTimeField(null=True, blank=True)),
                ('lunes_fin', models.DateTimeField(null=True, blank=True)),
                ('martes_inicio', models.DateTimeField(null=True, blank=True)),
                ('martes_fin', models.DateTimeField(null=True, blank=True)),
                ('miercoles_inicio', models.DateTimeField(null=True, blank=True)),
                ('miercoles_fin', models.DateTimeField(null=True, blank=True)),
                ('jueves_inicio', models.DateTimeField(null=True, blank=True)),
                ('jueves_fin', models.DateTimeField(null=True, blank=True)),
                ('viernes_inicio', models.DateTimeField(null=True, blank=True)),
                ('viernes_fin', models.DateTimeField(null=True, blank=True)),
                ('sabado_inicio', models.DateTimeField(null=True, blank=True)),
                ('sabado_fin', models.DateTimeField(null=True, blank=True)),
                ('domingo_inicio', models.DateTimeField(null=True, blank=True)),
                ('domingo_fin', models.DateTimeField(null=True, blank=True)),
                ('nutriologo', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
