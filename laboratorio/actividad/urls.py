from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActividadViewSet, ActividadTareaViewSet

router = DefaultRouter()
router.register(r'actividades', ActividadViewSet, basename='actividad')
router.register(r'actividad-tareas', ActividadTareaViewSet, basename='actividad-tarea')

urlpatterns = [
    path('', include(router.urls)),
]
