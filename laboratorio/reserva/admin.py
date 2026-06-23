from django.contrib import admin
from .models import Reserva, Docente

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ('id', 'laboratorio', 'docente_nombre', 'fecha', 'hora_inicio', 'hora_fin', 'id_aux')
    list_filter = ('fecha', 'laboratorio')
    search_fields = ('docente_nombre', 'motivo')

