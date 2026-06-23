from django.db import models

class Ubicacion(models.Model):
    ubicacion = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ubicacion'
        verbose_name = 'Ubicación'
        verbose_name_plural = 'Ubicaciones'

    def __str__(self):
        return self.ubicacion or f'Ubicacion #{self.id}'
