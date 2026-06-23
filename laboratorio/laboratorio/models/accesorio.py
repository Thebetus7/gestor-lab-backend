from django.db import models

class Accesorio(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'Accesorio'
        verbose_name = 'Accesorio'
        verbose_name_plural = 'Accesorios'

    def __str__(self):
        return self.nombre
