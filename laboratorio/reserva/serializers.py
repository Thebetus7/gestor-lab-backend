from rest_framework import serializers
from .models import Reserva, Docente
from laboratorio.laboratorio.models import Laboratorio
from django.contrib.auth import get_user_model

User = get_user_model()

class DocenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Docente
        fields = ['id', 'nombre']

class ReservaSerializer(serializers.ModelSerializer):
    laboratorio_nombre = serializers.CharField(source='laboratorio.nombre', read_only=True)
    auxiliar_username = serializers.CharField(source='id_aux.username', read_only=True)

    class Meta:
        model = Reserva
        fields = [
            'id',
            'laboratorio',
            'laboratorio_nombre',
            'docente_nombre',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'motivo',
            'id_aux',
            'auxiliar_username'
        ]

class ReservaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = [
            'id',
            'laboratorio',
            'docente_nombre',
            'fecha',
            'hora_inicio',
            'hora_fin',
            'motivo',
            'id_aux'
        ]

    def validate(self, attrs):
        hora_inicio = attrs.get('hora_inicio')
        hora_fin = attrs.get('hora_fin')
        fecha = attrs.get('fecha')
        laboratorio = attrs.get('laboratorio')

        # 1. Validar que la hora de inicio sea menor a la hora de fin
        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise serializers.ValidationError({
                "hora_fin": "La hora de fin debe ser posterior a la hora de inicio."
            })

        # 2. Validar traslape de horarios para el mismo laboratorio en la misma fecha
        if laboratorio and fecha and hora_inicio and hora_fin:
            queryset = Reserva.objects.filter(
                laboratorio=laboratorio,
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            )

            # Excluir la instancia actual si es una actualización
            if self.instance:
                queryset = queryset.exclude(id=self.instance.id)

            if queryset.exists():
                raise serializers.ValidationError(
                    "Ya existe una reserva registrada para este laboratorio en el horario seleccionado."
                )

        return attrs
