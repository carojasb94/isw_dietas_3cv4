# -*- encoding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, password, is_staff, is_superuser, is_active=False, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(username=username, email=email, is_active=is_active,
                          is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password=None, is_active=True, **extra_fields):
        # print('creando usuario')
        return self._create_user(username, email, password, False, False, is_active=True, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True, is_active=True, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=40, unique=True)
    nombre = models.CharField(max_length=40, blank=True)
    apellidos = models.CharField(max_length=40, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)
    status = models.BooleanField(default=False)  # para validar al usuario
    niveles = (("nutriologo", "nutriologo"),
               ("paciente", "paciente"),
               )
    tipo = models.CharField(choices=niveles, max_length=30, default="inactivo")
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_nutriologo = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    @property
    def get_short_name(self):
        if self.nombre != "":
            return self.nombre
        elif self.username != "":
            return self.username
        else:
            return self.email

    @property
    def get_full_name(self):
        if self.nombre != "":
            return self.nombre + " " + self.apellidos
        elif self.username != "":
            return self.username
        else:
            return str(self.email)

    def __str__(self):
        return self.get_short_name

    def __unicode__(self):
        return self.get_short_name


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = Usuario.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except Usuario.DoesNotExist as e:
            return None

    def get_user(self, username):
        try:
            return Usuario.objects.get(pk=username)
        except Usuario.DoesNotExist as e:
            return None

    def __str__(self):
        return str(self)
