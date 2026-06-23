import json
from rest_framework import serializers
from ..models import Ubicacion

class UbicacionSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(required=True)
    lng = serializers.FloatField(required=True)
    radio = serializers.FloatField(required=True)

    class Meta:
        model = Ubicacion
        fields = ['id', 'lat', 'lng', 'radio']

    def to_representation(self, instance):
        # Convertir el string JSON guardado en el TextField a campos individuales
        try:
            data = json.loads(instance.ubicacion) if instance.ubicacion else {}
        except Exception:
            data = {}
        
        return {
            'id': instance.id,
            'lat': data.get('lat', -17.783), # valores por defecto en Bolivia
            'lng': data.get('lng', -63.182),
            'radio': data.get('radio', 100.0)
        }

    def create(self, validated_data):
        # Convertir lat, lng, radio a string JSON
        ubicacion_data = {
            'lat': validated_data.get('lat'),
            'lng': validated_data.get('lng'),
            'radio': validated_data.get('radio')
        }
        # Guardar en base de datos
        instance = Ubicacion.objects.create(ubicacion=json.dumps(ubicacion_data))
        return instance

    def update(self, instance, validated_data):
        ubicacion_data = {
            'lat': validated_data.get('lat'),
            'lng': validated_data.get('lng'),
            'radio': validated_data.get('radio')
        }
        instance.ubicacion = json.dumps(ubicacion_data)
        instance.save()
        return instance
