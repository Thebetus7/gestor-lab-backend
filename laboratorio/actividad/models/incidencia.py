from django.db import models
from django.conf import settings
from laboratorio.laboratorio.models import Laboratorio, Accesorio

class Incidencia(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    prioridad = models.TextField(null=True, blank=True)
    id_lab = models.ForeignKey(
        Laboratorio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_lab',
        related_name='incidencias'
    )
    id_accesorio = models.ForeignKey(
        Accesorio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_accesorio',
        related_name='incidencias'
    )
    resuelto = models.BooleanField(null=True, blank=True)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_user',
        related_name='incidencias'
    )

    class Meta:
        db_table = 'incidencia'
        verbose_name = 'Incidencia'
        verbose_name_plural = 'Incidencias'

    def __str__(self):
        return self.descripcion or f'Incidencia #{self.id}'
