from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, CustomTokenObtainPairSerializer, RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

from django.contrib.auth.models import Group
from .models import CustomUser

class UserManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.has_role('admin') and not request.user.is_superuser:
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
        
        users = CustomUser.objects.filter(is_deleted=False).order_by('id')
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.has_role('admin') and not request.user.is_superuser:
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
            
        username = request.data.get('username')
        email = request.data.get('email', '')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        role = request.data.get('role')

        if not username or not password or not role:
            return Response({"detail": "Usuario, contraseña y rol son requeridos."}, status=status.HTTP_400_BAD_REQUEST)

        if CustomUser.objects.filter(username=username).exists():
            return Response({"detail": "El nombre de usuario ya existe."}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetailManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        if not request.user.has_role('admin') and not request.user.is_superuser:
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            user = CustomUser.objects.get(pk=pk, is_deleted=False)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if user == request.user and 'is_active' in request.data and not request.data.get('is_active', True):
            return Response({"detail": "No puedes desactivarte a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)

        if 'is_active' in request.data:
            user.is_active = request.data['is_active']
        if 'email' in request.data:
            user.email = request.data['email']
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        
        if 'role' in request.data:
            new_role = request.data['role']
            user.groups.clear()
            group, _ = Group.objects.get_or_create(name=new_role)
            user.groups.add(group)

        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def delete(self, request, pk):
        if not request.user.has_role('admin') and not request.user.is_superuser:
            return Response({"detail": "No tiene permiso para realizar esta acción."}, status=status.HTTP_403_FORBIDDEN)
            
        try:
            user = CustomUser.objects.get(pk=pk, is_deleted=False)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        if user == request.user:
            return Response({"detail": "No puedes eliminarte a ti mismo."}, status=status.HTTP_400_BAD_REQUEST)

        user.is_deleted = True
        user.is_active = False
        user.save()
        
        return Response({"message": "Usuario eliminado exitosamente (soft-delete)."}, status=status.HTTP_200_OK)
