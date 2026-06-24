from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LaboratorioViewSet, UbicacionViewSet, AccesorioViewSet, chatbot_context

router = DefaultRouter()
router.register(r'laboratorios', LaboratorioViewSet, basename='laboratorio')
router.register(r'ubicacion', UbicacionViewSet, basename='ubicacion')
router.register(r'accesorios', AccesorioViewSet, basename='accesorio')

urlpatterns = [
    path('chatbot/context/', chatbot_context, name='chatbot_context'),
    path('', include(router.urls)),
]

