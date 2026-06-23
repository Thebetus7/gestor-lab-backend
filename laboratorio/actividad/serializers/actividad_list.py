from rest_framework import serializers
from ..models import Actividad

class ActividadListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = ['id', 'descripcion', 'tiempo', 'is_active']
