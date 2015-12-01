# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, verbose_name='last login', null=True)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(unique=True, max_length=40)),
                ('nombre', models.CharField(max_length=40, blank=True)),
                ('apellidos', models.CharField(max_length=40, blank=True)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('status', models.BooleanField(default=False)),
                ('tipo', models.CharField(default='inactivo', max_length=30, choices=[('nutriologo', 'nutriologo'), ('paciente', 'paciente')])),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_nutriologo', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, verbose_name='groups', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', to='auth.Group', related_query_name='user', related_name='user_set')),
                ('user_permissions', models.ManyToManyField(blank=True, verbose_name='user permissions', help_text='Specific permissions for this user.', to='auth.Permission', related_query_name='user', related_name='user_set')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
