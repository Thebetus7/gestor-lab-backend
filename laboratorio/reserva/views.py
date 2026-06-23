from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime

from .models import Reserva, Docente
from .serializers import ReservaSerializer, ReservaCreateSerializer, DocenteSerializer
from laboratorio.laboratorio.models import Laboratorio

class DocenteViewSet(viewsets.ModelViewSet):
    queryset = Docente.objects.all().order_by('nombre')
    serializer_class = DocenteSerializer

    def get_permissions(self):
        # Permitir listar sugerencias a cualquier usuario, pero solo los autenticados pueden borrar/editar
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAuthenticated()]

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all().order_by('-fecha', '-hora_inicio')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReservaCreateSerializer
        return ReservaSerializer

    def get_permissions(self):
        # Permisos mixtos: Listado, detalle y estado de disponibilidad son públicos (AllowAny)
        # para que la app móvil y visitantes los puedan consultar sin token de acceso.
        if self.action in ['list', 'retrieve', 'estado_espacios']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        # Asignar automáticamente el usuario autenticado como id_aux
        reserva = serializer.save(id_aux=self.request.user)
        
        # Registrar el docente en el catálogo si es un nombre nuevo
        docente_nombre = reserva.docente_nombre.strip()
        if docente_nombre:
            Docente.objects.get_or_create(nombre=docente_nombre)

    def perform_update(self, serializer):
        reserva = serializer.save()
        
        # Registrar el docente en el catálogo si es un nombre nuevo
        docente_nombre = reserva.docente_nombre.strip()
        if docente_nombre:
            Docente.objects.get_or_create(nombre=docente_nombre)

    @action(detail=False, methods=['get'], url_path='estado-espacios')
    def estado_espacios(self, request):
        fecha_str = request.query_params.get('fecha')
        
        if fecha_str:
            try:
                # Intentamos parsear la fecha YYYY-MM-DD
                fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
            except ValueError:
                return Response(
                    {"error": "Formato de fecha inválido. Debe ser YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            fecha = timezone.now().date()

        laboratorios = Laboratorio.objects.filter(is_deleted=False).order_by('nombre')
        resultado = []

        for lab in laboratorios:
            # Obtener las reservas de este laboratorio en la fecha dada
            reservas_lab = Reserva.objects.filter(laboratorio=lab, fecha=fecha).order_by('hora_inicio')
            
            reservas_data = []
            for r in reservas_lab:
                reservas_data.append({
                    "id": r.id,
                    "docente": r.docente_nombre,
                    "hora_inicio": r.hora_inicio.strftime('%H:%M'),
                    "hora_fin": r.hora_fin.strftime('%H:%M'),
                    "motivo": r.motivo
                })

            estado = "libre" if not reservas_lab.exists() else "parcial"

            resultado.append({
                "id": lab.id,
                "nombre": lab.nombre,
                "capacidad": lab.capacidad,
                "estado": estado,
                "reservas": reservas_data
            })

        return Response(resultado, status=status.HTTP_200_OK)
