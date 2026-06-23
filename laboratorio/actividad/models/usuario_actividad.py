from django.db import models
from django.conf import settings
from .actividad import Actividad
from laboratorio.laboratorio.models import Laboratorio

class UsuarioActividad(models.Model):
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_user',
        related_name='usuario_actividades'
    )
    id_actividad = models.ForeignKey(
        Actividad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_actividad',
        related_name='usuario_actividades'
    )
    id_lab = models.ForeignKey(
        Laboratorio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_lab',
        related_name='usuario_actividades'
    )

    class Meta:
        db_table = 'UsuarioActividad'
        verbose_name = 'Usuario-Actividad'
        verbose_name_plural = 'Usuario-Actividades'

    def __str__(self):
        return f'UsuarioActividad #{self.id}'
