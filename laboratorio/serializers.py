from rest_framework import serializers
from .models import Actividad, Tarea, ActividadTarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'tarea', 'id_actividad']

class ActividadTareaSerializer(serializers.ModelSerializer):
    tarea_descripcion = serializers.CharField(source='id_tarea.tarea', read_only=True)
    
    class Meta:
        model = ActividadTarea
        fields = ['id', 'id_activ', 'id_tarea', 'tarea_descripcion', 'observacion', 'estado']

class ActividadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'descripcion', 'tiempo', 'is_active']

class ActividadDetailSerializer(serializers.ModelSerializer):
    actividad_tareas = ActividadTareaSerializer(many=True, read_only=True)

    class Meta:
        model = Actividad
        fields = ['id', 'descripcion', 'tiempo', 'is_active', 'actividad_tareas']

class ActividadCreateSerializer(serializers.Serializer):
    descripcion = serializers.CharField(required=False, allow_blank=True)
    tiempo = serializers.TimeField(required=False, allow_null=True)
    tareas = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )

    def create(self, validated_data):
        tareas_data = validated_data.pop('tareas', [])
        
        # 1. Crear Actividad
        actividad = Actividad.objects.create(
            descripcion=validated_data.get('descripcion'),
            tiempo=validated_data.get('tiempo')
        )

        # 2. Crear Tareas y ActividadTarea por cada string recibido
        for tarea_desc in tareas_data:
            if tarea_desc.strip():
                # Crear Tarea
                tarea = Tarea.objects.create(
                    tarea=tarea_desc.strip(),
                    id_actividad=actividad
                )
                # Crear tracking en ActividadTarea (estado inicial)
                ActividadTarea.objects.create(
                    id_activ=actividad,
                    id_tarea=tarea,
                    estado='espera', # Estado inicial por defecto
                    observacion=''
                )

        return actividad
