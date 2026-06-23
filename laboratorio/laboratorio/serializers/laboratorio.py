from rest_framework import serializers
from ..models import Laboratorio
from .accesorio import AccesorioSerializer

class LaboratorioSerializer(serializers.ModelSerializer):
    maquinas_count = serializers.SerializerMethodField()
    accesorios = AccesorioSerializer(many=True, read_only=True)

    class Meta:
        model = Laboratorio
        fields = ['id', 'nombre', 'capacidad', 'filas', 'columnas', 'maquinas_count', 'accesorios']

    def get_maquinas_count(self, obj):
        return obj.maquinas.count()
