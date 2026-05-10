from django.db import models
from django.conf import settings

class Reserva(models.Model):
    motivo = models.TextField(null=True, blank=True)
    id_aux = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_aux',
        related_name='reservas'
    )

    class Meta:
        db_table = 'reserva'
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'

    def __str__(self):
        return self.motivo or f'Reserva #{self.id}'
