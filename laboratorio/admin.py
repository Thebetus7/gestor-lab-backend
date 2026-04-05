from django.contrib import admin
from .models import (
    Laboratorio, Actividad, Tarea, ActividadTarea,
    UsuarioActividad, Reserva, Notificacion, Maquina,
    Incidencia, Asistencia, Ubicacion
)

admin.site.register(Laboratorio)
admin.site.register(Actividad)
admin.site.register(Tarea)
admin.site.register(ActividadTarea)
admin.site.register(UsuarioActividad)
admin.site.register(Reserva)
admin.site.register(Notificacion)
admin.site.register(Maquina)
admin.site.register(Incidencia)
admin.site.register(Asistencia)
admin.site.register(Ubicacion)
