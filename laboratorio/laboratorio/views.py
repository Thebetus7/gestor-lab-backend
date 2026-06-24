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
        from laboratorio.reserva.models import Reserva, Docente
        from laboratorio.actividad.models.incidencia import Incidencia
        from laboratorio.actividad.models.actividad import Actividad
        from django.contrib.auth import get_user_model
        from django.utils import timezone
        
        User = get_user_model()
        labs = Laboratorio.objects.filter(is_deleted=False)
        context_lines = []
        context_lines.append("INFORMACIÓN GLOBAL DEL SISTEMA DE GESTORLAB:")
        
        # 1. Información de Usuarios (Personal)
        context_lines.append("\n--- PERSONAL Y USUARIOS DEL SISTEMA ---")
        usuarios = User.objects.filter(is_deleted=False, is_active=True)
        for u in usuarios:
            roles = ", ".join(u.groups.values_list('name', flat=True)) if u.groups.exists() else "Sin rol"
            context_lines.append(f"- Usuario: {u.username} (Nombre: {u.first_name} {u.last_name}) - Roles: {roles}")
            
        # 2. Información de Docentes
        context_lines.append("\n--- DOCENTES REGISTRADOS ---")
        docentes = Docente.objects.all()
        docentes_nombres = [d.nombre for d in docentes]
        context_lines.append(f"Total: {len(docentes_nombres)}. Lista: {', '.join(docentes_nombres) if docentes_nombres else 'Ninguno'}")
        
        # 3. Información de Actividades de Mantenimiento
        context_lines.append("\n--- ACTIVIDADES DE MANTENIMIENTO GLOBALES ---")
        actividades = Actividad.objects.filter(is_active=True)
        for a in actividades:
            tiempo_str = a.tiempo.strftime('%H:%M') if a.tiempo else "No especificado"
            context_lines.append(f"- Actividad: {a.descripcion} (Tiempo estimado: {tiempo_str})")

        # 4. Información de Laboratorios, Reservas e Incidencias
        context_lines.append("\n--- ESTADO DE LOS LABORATORIOS ---")
        context_lines.append(f"Cantidad total de laboratorios activos: {labs.count()}")
        
        for lab in labs:
            context_lines.append(f"\n* Laboratorio: {lab.nombre} *")
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
            
            # Reservas futuras o de hoy en este laboratorio
            reservas = Reserva.objects.filter(laboratorio=lab, fecha__gte=timezone.now().date()).order_by('fecha', 'hora_inicio')
            if reservas.exists():
                context_lines.append("  Reservas programadas:")
                for r in reservas:
                    context_lines.append(f"    - {r.fecha} de {r.hora_inicio.strftime('%H:%M')} a {r.hora_fin.strftime('%H:%M')} - Docente: {r.docente_nombre} - Motivo: {r.motivo}")
            else:
                context_lines.append("  Reservas programadas: Ninguna en los próximos días")
                
            # Incidencias no resueltas en este laboratorio
            incidencias = Incidencia.objects.filter(id_lab=lab, resuelto=False)
            if incidencias.exists():
                context_lines.append("  Incidencias / Problemas reportados (SIN RESOLVER):")
                for i in incidencias:
                    acc_nombre = f" en accesorio {i.id_accesorio.nombre}" if i.id_accesorio else ""
                    prioridad = f"[{i.prioridad}]" if i.prioridad else ""
                    context_lines.append(f"    - {prioridad} {i.descripcion}{acc_nombre}")
            else:
                context_lines.append("  Incidencias: Todo funcionando correctamente")
                
        context_text = "\n".join(context_lines)
        return Response({"context": context_text}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


