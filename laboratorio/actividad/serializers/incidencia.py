from rest_framework import serializers
from ..models import Incidencia
from laboratorio.laboratorio.models import Laboratorio

class IncidenciaSerializer(serializers.ModelSerializer):
    nombre_lab = serializers.SerializerMethodField(read_only=True)
    username_usuario = serializers.SerializerMethodField(read_only=True)
    nombre_accesorio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Incidencia
        fields = ['id', 'descripcion', 'prioridad', 'id_lab', 'nombre_lab', 'resuelto', 'id_user', 'username_usuario', 'id_accesorio', 'nombre_accesorio']
        read_only_fields = ['id_user']

    def get_nombre_lab(self, obj):
        return obj.id_lab.nombre if obj.id_lab else None
        
    def get_nombre_accesorio(self, obj):
        return obj.id_accesorio.nombre if obj.id_accesorio else None

    def get_username_usuario(self, obj):
        return obj.id_user.username if obj.id_user else None
