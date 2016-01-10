# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mensaje',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mensaje', models.CharField(default=b'', max_length=100, blank=True)),
                ('fecha', models.DateTimeField(default=datetime.datetime(2016, 1, 7, 20, 28, 27, 525785))),
                ('destinatario', models.ForeignKey(related_name='UsuarioDestinatario', to=settings.AUTH_USER_MODEL)),
                ('remitente', models.ForeignKey(related_name='UsuarioRemitente', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
