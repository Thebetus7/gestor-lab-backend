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


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['GET'])
@permission_classes([AllowAny])
def chatbot_context(request):
    try:
        from django.conf import settings
        import os
        
        file_path = os.path.join(settings.BASE_DIR, 'gestorlab-info.txt')
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                context_text = f.read()
        else:
            context_text = "La información institucional de GestorLab no está disponible."
            
        return Response({"context": context_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


