from django.db import models
from django.conf import settings

class Asistencia(models.Model):
    entrada = models.TimeField(null=True, blank=True)
    salida = models.TimeField(null=True, blank=True)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_user',
        related_name='asistencias'
    )

    class Meta:
        db_table = 'Asistencia'
        verbose_name = 'Asistencia'
        verbose_name_plural = 'Asistencias'

    def __str__(self):
        return f'Asistencia #{self.id}'
