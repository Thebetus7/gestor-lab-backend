from rest_framework import serializers
from .models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='id_user.username', read_only=True)
    first_name = serializers.CharField(source='id_user.first_name', read_only=True)
    last_name = serializers.CharField(source='id_user.last_name', read_only=True)

    class Meta:
        model = Asistencia
        fields = ['id', 'fecha', 'entrada', 'salida', 'id_user', 'username', 'first_name', 'last_name']
