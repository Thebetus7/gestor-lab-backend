from django.db import models

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
