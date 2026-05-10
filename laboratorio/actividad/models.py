from django.db import models
from django.conf import settings
from laboratorio.laboratorio.models import Laboratorio

class Actividad(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    tiempo = models.TimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Actividad'
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

    def __str__(self):
        return self.descripcion or f'Actividad #{self.id}'

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
