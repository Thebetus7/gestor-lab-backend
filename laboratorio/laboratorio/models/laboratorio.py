from django.db import models
from .accesorio import Accesorio

class Laboratorio(models.Model):
    nombre = models.TextField(null=True, blank=True)
    capacidad = models.TextField(null=True, blank=True)
    filas = models.IntegerField(default=0)
    columnas = models.IntegerField(default=0)
    is_deleted = models.BooleanField(default=False)
    accesorios = models.ManyToManyField(Accesorio, blank=True, related_name='laboratorios')

    class Meta:
        db_table = 'Laboratorio'
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'

    def __str__(self):
        return self.nombre or f'Laboratorio #{self.id}'
