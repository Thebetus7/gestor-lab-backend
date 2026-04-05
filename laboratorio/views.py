from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Actividad, ActividadTarea
from .serializers import (
    ActividadListSerializer,
    ActividadDetailSerializer,
    ActividadCreateSerializer,
    ActividadTareaSerializer
)

class ActividadViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Actividad.objects.filter(is_active=True).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create':
            return ActividadCreateSerializer
        if self.action == 'retrieve':
            return ActividadDetailSerializer
        return ActividadListSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        actividad = serializer.save()
        
        # Devolver el detalle de la actividad recién creada
        detail_serializer = ActividadDetailSerializer(actividad)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        # Soft delete
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActividadTareaViewSet(viewsets.ModelViewSet):
    """
    Gestiona el estado/observaciones de las tareas dentro de una actividad.
    Principalmente usado para actualizar el estado por los auxiliares o jefes.
    """
    permission_classes = [IsAuthenticated]
    queryset = ActividadTarea.objects.all().order_by('id')
    serializer_class = ActividadTareaSerializer
    
    # Permitir actualizar sólo observacion o estado si es necesario
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
