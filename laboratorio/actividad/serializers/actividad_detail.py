from rest_framework import serializers
from ..models import Actividad
from .actividad_tarea import ActividadTareaSerializer

class ActividadDetailSerializer(serializers.ModelSerializer):
    actividad_tareas = ActividadTareaSerializer(many=True, read_only=True)
    laboratorios = serializers.SerializerMethodField()

    class Meta:
        model = Actividad
        fields = ['id', 'descripcion', 'tiempo', 'is_active', 'actividad_tareas', 'laboratorios']

    def get_laboratorios(self, obj):
        labs = []
        for ua in obj.usuario_actividades.select_related('id_lab').all():
            if ua.id_lab and ua.id_lab not in labs:
                labs.append(ua.id_lab)
        return [{'id': l.id, 'nombre': l.nombre} for l in labs]
