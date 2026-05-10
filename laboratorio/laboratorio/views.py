from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Laboratorio
from .serializers import LaboratorioSerializer, LaboratorioCreateSerializer

class LaboratorioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Laboratorio.objects.all().order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create':
            return LaboratorioCreateSerializer
        return LaboratorioSerializer
