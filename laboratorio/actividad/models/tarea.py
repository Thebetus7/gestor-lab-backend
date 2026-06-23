from django.db import models
from .actividad import Actividad

class Tarea(models.Model):
    tarea = models.TextField(null=True, blank=True)
    id_actividad = models.ForeignKey(
        Actividad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_actividad',
        related_name='tareas'
    )

    class Meta:
        db_table = 'Tarea'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'

    def __str__(self):
        return self.tarea or f'Tarea #{self.id}'
