from rest_framework import serializers
from .models import Laboratorio, Maquina

class LaboratorioSerializer(serializers.ModelSerializer):
    maquinas_count = serializers.SerializerMethodField()

    class Meta:
        model = Laboratorio
        fields = ['id', 'nombre', 'capacidad', 'filas', 'columnas', 'maquinas_count']

    def get_maquinas_count(self, obj):
        return obj.maquinas.count()

class LaboratorioCreateSerializer(serializers.ModelSerializer):
    maquinas_count = serializers.IntegerField(write_only=True, required=False, default=0)

    class Meta:
        model = Laboratorio
        fields = ['id', 'nombre', 'capacidad', 'filas', 'columnas', 'maquinas_count']

    def create(self, validated_data):
        maquinas_count = validated_data.pop('maquinas_count', 0)
        laboratorio = Laboratorio.objects.create(**validated_data)
        
        maquinas_a_crear = [Maquina(id_lab=laboratorio) for _ in range(maquinas_count)]
        if maquinas_a_crear:
            Maquina.objects.bulk_create(maquinas_a_crear)
            
        return laboratorio
