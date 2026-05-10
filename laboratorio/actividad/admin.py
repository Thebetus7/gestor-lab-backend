from django.contrib import admin
from .models import Actividad, Tarea, ActividadTarea, UsuarioActividad, Incidencia

admin.site.register(Actividad)
admin.site.register(Tarea)
admin.site.register(ActividadTarea)
admin.site.register(UsuarioActividad)
admin.site.register(Incidencia)
