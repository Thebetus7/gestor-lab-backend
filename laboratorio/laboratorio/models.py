from django.db import models

class Laboratorio(models.Model):
    nombre = models.TextField(null=True, blank=True)
    capacidad = models.TextField(null=True, blank=True)
    filas = models.IntegerField(default=0)
    columnas = models.IntegerField(default=0)

    class Meta:
        db_table = 'Laboratorio'
        verbose_name = 'Laboratorio'
        verbose_name_plural = 'Laboratorios'

    def __str__(self):
        return self.nombre or f'Laboratorio #{self.id}'

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

class Ubicacion(models.Model):
    ubicacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.ubicacion or f'Ubicacion #{self.id}'
