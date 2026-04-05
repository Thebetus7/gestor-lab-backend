from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'roles')

    def get_roles(self, obj):
        return obj.get_roles()
