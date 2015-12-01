# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dieta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, null=True, editable=False)),
                ('codigo', models.CharField(default='', max_length=10)),
            ],
        ),
    ]
