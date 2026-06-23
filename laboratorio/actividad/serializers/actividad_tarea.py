from rest_framework import serializers
from ..models import ActividadTarea

class ActividadTareaSerializer(serializers.ModelSerializer):
    tarea_descripcion = serializers.CharField(source='id_tarea.tarea', read_only=True)
    
    class Meta:
        model = ActividadTarea
        fields = ['id', 'id_activ', 'id_tarea', 'tarea_descripcion', 'observacion', 'estado']
