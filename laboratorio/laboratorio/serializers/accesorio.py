from rest_framework import serializers
from ..models import Accesorio

class AccesorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accesorio
        fields = ['id', 'nombre', 'descripcion']
