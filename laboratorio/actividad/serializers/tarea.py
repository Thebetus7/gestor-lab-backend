from rest_framework import serializers
from ..models import Tarea

class TareaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarea
        fields = ['id', 'tarea', 'id_actividad']
