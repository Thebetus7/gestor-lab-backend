from rest_framework import serializers
from ..models import Laboratorio, Maquina, Accesorio
from .laboratorio import LaboratorioSerializer

class LaboratorioCreateSerializer(serializers.ModelSerializer):
    maquinas_count = serializers.IntegerField(required=False, default=0)
    accesorios_ids = serializers.PrimaryKeyRelatedField(
        queryset=Accesorio.objects.filter(is_deleted=False), 
        many=True, 
        required=False, 
        write_only=True,
        source='accesorios'
    )

    class Meta:
        model = Laboratorio
        fields = ['id', 'nombre', 'capacidad', 'filas', 'columnas', 'maquinas_count', 'accesorios_ids']

    def create(self, validated_data):
        maquinas_count = validated_data.pop('maquinas_count', 0)
        accesorios = validated_data.pop('accesorios', [])
        
        laboratorio = Laboratorio.objects.create(**validated_data)
        
        if accesorios:
            laboratorio.accesorios.set(accesorios)
        
        maquinas_a_crear = [Maquina(id_lab=laboratorio) for _ in range(maquinas_count)]
        if maquinas_a_crear:
            Maquina.objects.bulk_create(maquinas_a_crear)
            
        return laboratorio

    def update(self, instance, validated_data):
        maquinas_count = validated_data.pop('maquinas_count', None)
        accesorios = validated_data.pop('accesorios', None)
        
        # Actualizar campos básicos de Laboratorio
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if accesorios is not None:
            instance.accesorios.set(accesorios)

        # Sincronizar la cantidad de máquinas asociadas
        if maquinas_count is not None:
            maquinas_actuales = instance.maquinas.all()
            cantidad_actual = maquinas_actuales.count()
            
            if maquinas_count > cantidad_actual:
                # Crear nuevas máquinas
                diferencia = maquinas_count - cantidad_actual
                nuevas = [Maquina(id_lab=instance) for _ in range(diferencia)]
                Maquina.objects.bulk_create(nuevas)
            elif maquinas_count < cantidad_actual:
                # Eliminar las sobrantes (empezando por las últimas creadas)
                diferencia = cantidad_actual - maquinas_count
                maquinas_a_eliminar = maquinas_actuales.order_by('-id')[:diferencia]
                Maquina.objects.filter(id__in=[m.id for m in maquinas_a_eliminar]).delete()
                
        return instance

    def to_representation(self, instance):
        # Utilizar LaboratorioSerializer para retornar el formato de respuesta estructurado de lectura
        return LaboratorioSerializer(instance).data
