from rest_framework import serializers
from ..models import Actividad, Tarea, ActividadTarea, UsuarioActividad
from laboratorio.laboratorio.models import Laboratorio

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
        
        actividad = Actividad.objects.create(
            descripcion=validated_data.get('descripcion'),
        )

        for tarea_desc in tareas_data:
            if tarea_desc.strip():
                tarea = Tarea.objects.create(
                    tarea=tarea_desc.strip(),
                    id_actividad=actividad
                )
                ActividadTarea.objects.create(
                    id_activ=actividad,
                    id_tarea=tarea,
                    estado='espera',
                    observacion=''
                )

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
