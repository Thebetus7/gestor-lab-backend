from rest_framework import serializers
from .models import Actividad, Tarea, ActividadTarea, Laboratorio, UsuarioActividad

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
    tareas = serializers.ListField(
        child=serializers.CharField(), required=False, allow_empty=True
    )
    laboratorios = serializers.ListField(
        child=serializers.IntegerField(), required=False, allow_empty=True
    )

    def create(self, validated_data):
        tareas_data = validated_data.pop('tareas', [])
        laboratorios_ids = validated_data.pop('laboratorios', [])
        
        # 1. Crear Actividad (sin campo tiempo)
        actividad = Actividad.objects.create(
            descripcion=validated_data.get('descripcion'),
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

        # 3. Relacionar con laboratorios (UsuarioActividad)
        user = self.context['request'].user
        for lab_id in laboratorios_ids:
            try:
                lab = Laboratorio.objects.get(id=lab_id)
                UsuarioActividad.objects.create(
                    id_user=user,
                    id_actividad=actividad,
                    id_lab=lab
                )
            except Laboratorio.DoesNotExist:
                continue

        return actividad
