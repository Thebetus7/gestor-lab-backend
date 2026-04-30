from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from .models import CustomUser

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        from django.db.models import Q
        username = attrs.get(self.username_field)

        # Verificar si el usuario existe antes de validar la contraseña
        user = CustomUser.objects.filter(Q(username=username) | Q(email=username)).first()
        if not user:
            # Lanzamos un error específico si el usuario no se encuentra
            raise exceptions.AuthenticationFailed(
                "El correo electrónico o usuario ingresado no existe.",
                "no_user"
            )
            
        attrs[self.username_field] = user.username

        try:
            # Si el usuario existe, llamamos al método original para validar contraseña y generar tokens
            return super().validate(attrs)
        except exceptions.AuthenticationFailed:
            # Si falla aquí, el usuario existía pero la contraseña estaba mal
            raise exceptions.AuthenticationFailed(
                "La contraseña ingresada es incorrecta.",
                "invalid_password"
            )

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
