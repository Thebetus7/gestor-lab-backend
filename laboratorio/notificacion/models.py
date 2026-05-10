from django.db import models
from django.conf import settings

class Notificacion(models.Model):
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_user',
        related_name='notificaciones'
    )

    class Meta:
        db_table = 'Notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'

    def __str__(self):
        return f'Notificacion #{self.id}'
