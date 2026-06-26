from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        from django.db.models import Q
        username = attrs.get(self.username_field)

        user = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if not user:
            raise exceptions.AuthenticationFailed(
                "El correo electrónico o usuario ingresado no existe.",
                "no_user"
            )
            
        attrs[self.username_field] = user.username

        try:
            res = super().validate(attrs)
        except exceptions.AuthenticationFailed:
            raise exceptions.AuthenticationFailed(
                "La contraseña ingresada es incorrecta.",
                "invalid_password"
            )

        # Verificar ubicación si es auxiliar
        if user.has_role('auxiliar'):
            request = self.context.get('request')
            if not request:
                raise exceptions.AuthenticationFailed("No se pudo obtener la solicitud.")

            lat = request.data.get('latitude')
            lng = request.data.get('longitude')

            if lat is None or lng is None:
                raise exceptions.AuthenticationFailed("La ubicación GPS es obligatoria para los auxiliares.")

            try:
                lat = float(lat)
                lng = float(lng)
            except (ValueError, TypeError):
                raise exceptions.AuthenticationFailed("Las coordenadas GPS no son válidas.")

            # Obtener ubicación configurada en el sistema
            from laboratorio.laboratorio.models import Ubicacion
            import json
            import math

            system_location_obj = Ubicacion.objects.first()
            if system_location_obj and system_location_obj.ubicacion:
                try:
                    loc_data = json.loads(system_location_obj.ubicacion)
                    sys_lat = float(loc_data.get('lat'))
                    sys_lng = float(loc_data.get('lng'))
                    sys_radio = float(loc_data.get('radio', 100.0))
                except Exception:
                    sys_lat, sys_lng, sys_radio = -17.783, -63.182, 100.0
            else:
                sys_lat, sys_lng, sys_radio = -17.783, -63.182, 100.0

            # Calcular distancia usando la fórmula de Haversine
            R = 6371000  # Radio de la Tierra en metros
            phi1 = math.radians(lat)
            phi2 = math.radians(sys_lat)
            delta_phi = math.radians(sys_lat - lat)
            delta_lambda = math.radians(sys_lng - lng)

            a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = R * c

            if distance > sys_radio:
                raise exceptions.AuthenticationFailed(
                    f"Usted se encuentra fuera del rango permitido. Distancia: {distance:.1f}m. Rango permitido: {sys_radio:.1f}m."
                )

            # Registrar asistencia de entrada si no existe hoy
            from django.utils import timezone
            from usuarios.auxiliar.models import Asistencia

            now = timezone.now()
            today = now.date()
            asistencia_existente = Asistencia.objects.filter(id_user=user, fecha=today).first()
            if not asistencia_existente:
                Asistencia.objects.create(
                    id_user=user,
                    fecha=today,
                    entrada=now.time()
                )

        return res

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'roles')

    def get_roles(self, obj):
        return obj.get_roles()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
