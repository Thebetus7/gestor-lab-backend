from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Laboratorio, Ubicacion, Accesorio
from .serializers import LaboratorioSerializer, LaboratorioCreateSerializer, UbicacionSerializer, AccesorioSerializer

class AccesorioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Accesorio.objects.filter(is_deleted=False).order_by('nombre')
    serializer_class = AccesorioSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LaboratorioViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Laboratorio.objects.filter(is_deleted=False).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return LaboratorioCreateSerializer
        return LaboratorioSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UbicacionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        # Intentar obtener la primera ubicación. Si no existe, crear una por defecto.
        ubicacion = Ubicacion.objects.first()
        if not ubicacion:
            ubicacion = Ubicacion.objects.create(ubicacion='{"lat": -17.783, "lng": -63.182, "radio": 100.0}')
        
        serializer = UbicacionSerializer(ubicacion)
        return Response(serializer.data)

    def create(self, request):
        # Si ya existe, actualizamos. Si no, creamos.
        ubicacion = Ubicacion.objects.first()
        if ubicacion:
            serializer = UbicacionSerializer(ubicacion, data=request.data)
        else:
            serializer = UbicacionSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

