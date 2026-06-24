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
        labs = Laboratorio.objects.filter(is_deleted=False)
        context_lines = []
        context_lines.append("INFORMACIÓN DEL SISTEMA DE GESTORLAB:")
        context_lines.append(f"Cantidad total de laboratorios activos: {labs.count()}")
        
        for lab in labs:
            context_lines.append(f"\n- Laboratorio: {lab.nombre}")
            context_lines.append(f"  Capacidad: {lab.capacidad} personas")
            context_lines.append(f"  Distribución: {lab.filas} filas x {lab.columnas} columnas")
            
            # Accesorios
            accesorios_list = [a.nombre for a in lab.accesorios.all() if not a.is_deleted]
            if accesorios_list:
                context_lines.append(f"  Accesorios disponibles: {', '.join(accesorios_list)}")
            else:
                context_lines.append("  Accesorios disponibles: Ninguno")
                
            # Máquinas
            maquinas_count = lab.maquinas.count()
            context_lines.append(f"  Máquinas instaladas: {maquinas_count}")
            
        context_text = "\n".join(context_lines)
        return Response({"context": context_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

