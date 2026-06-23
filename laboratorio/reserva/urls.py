from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReservaViewSet, DocenteViewSet

router = DefaultRouter()
router.register(r'reservas', ReservaViewSet, basename='reserva')
router.register(r'docentes', DocenteViewSet, basename='docente')

urlpatterns = [
    path('', include(router.urls)),
]

