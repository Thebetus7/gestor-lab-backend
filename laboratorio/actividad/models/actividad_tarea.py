from django.db import models
from .actividad import Actividad
from .tarea import Tarea

class ActividadTarea(models.Model):
    id_activ = models.ForeignKey(
        Actividad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_activ',
        related_name='actividad_tareas'
    )
    id_tarea = models.ForeignKey(
        Tarea,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_tarea',
        related_name='actividad_tareas'
    )
    observacion = models.TextField(null=True, blank=True)
    estado = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ActividadTarea'
        verbose_name = 'Actividad-Tarea'
        verbose_name_plural = 'Actividad-Tareas'

    def __str__(self):
        return f'ActividadTarea #{self.id}'
