from django.db import models
from .laboratorio import Laboratorio

class Maquina(models.Model):
    cod_activo = models.IntegerField(null=True, blank=True)
    id_lab = models.ForeignKey(
        Laboratorio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_lab',
        related_name='maquinas'
    )

    class Meta:
        db_table = 'Maquina'
        verbose_name = 'Máquina'
        verbose_name_plural = 'Máquinas'

    def __str__(self):
        return f'Maquina #{self.id} (activo: {self.cod_activo})'
