from django.db import models
from django.conf import settings
from django.utils import timezone
from laboratorio.laboratorio.models import Laboratorio

class Docente(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    
    class Meta:
        db_table = 'docente'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    laboratorio = models.ForeignKey(
        Laboratorio,
        on_delete=models.CASCADE,
        db_column='id_lab',
        related_name='reservas',
        null=True,
        blank=True
    )
    docente_nombre = models.CharField(max_length=255, default='')
    fecha = models.DateField(default=timezone.now)
    hora_inicio = models.TimeField(default='08:00')
    hora_fin = models.TimeField(default='10:00')
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
        return f"{self.docente_nombre} - {self.laboratorio} ({self.fecha})"


