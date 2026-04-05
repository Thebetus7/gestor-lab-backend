from django.db import models
from django.conf import settings


class Laboratorio(models.Model):
    nombre = models.TextField(null=True, blank=True)
    capacidad = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Laboratorio'
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'

    def __str__(self):
        return self.nombre or f'Laboratorio #{self.id}'


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
    # tareas como checkbox
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
    # describe simplemente lo que sucedió
    observacion = models.TextField(null=True, blank=True)
    # realizado, espera, problema
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


class Maquina(models.Model):
    # su ID activo
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


class Incidencia(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    # alta, media, baja
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


class Ubicacion(models.Model):
    ubicacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.ubicacion or f'Ubicacion #{self.id}'
