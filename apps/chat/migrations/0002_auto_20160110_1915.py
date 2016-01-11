# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensaje',
            name='fecha',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 10, 19, 15, 14, 615893)),
        ),
    ]
