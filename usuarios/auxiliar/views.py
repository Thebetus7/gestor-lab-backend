from rest_framework import viewsets, permissions
from .models import Asistencia
from .serializers import AsistenciaSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        queryset = Asistencia.objects.all().order_by('-fecha', '-entrada')
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(id_user_id=user_id)
        return queryset
