from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/usuarios/', include('usuarios.autenticacion.urls')),
    path('api/laboratorio/', include('laboratorio.laboratorio.urls')),
    path('api/actividad/', include('laboratorio.actividad.urls')),
    path('api/reserva/', include('laboratorio.reserva.urls')),
    path('api/notificacion/', include('laboratorio.notificacion.urls')),
    path('api/auxiliar/', include('usuarios.auxiliar.urls')),
]
