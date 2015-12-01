from datetime import date
from django.db import models

# Create your models here.
from django.utils.text import slugify
from apps.usuarios.models import Usuario


class Dieta(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(editable=False, max_length=100, null=True)
    codigo = models.CharField(max_length=10, default="")
    usuario = models.ForeignKey(Usuario)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.nombre + "-" + str(date.today()))
        super(Dieta, self).save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    def __unicode__(self):
        return self.nombre
