# 02. Detalle Técnico: Backend (Django)

Este documento detalla los cambios técnicos realizados en la capa del backend.

## 1. Modificaciones en Modelos (`usuarios/auxiliar/models.py`)

Se añadió el campo `fecha` para persistir el día correspondiente a la asistencia, desvinculando la lógica de hora de la fecha en sí.

```python
class Asistencia(models.Model):
    fecha = models.DateField(null=True, blank=True)
    entrada = models.TimeField(null=True, blank=True)
    salida = models.TimeField(null=True, blank=True)
    id_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_user',
        related_name='asistencias'
    )
```

## 2. Lógica de Autenticación y Geocercas (`usuarios/autenticacion/serializers.py`)

En `CustomTokenObtainPairSerializer.validate`, se intercepta la autenticación exitosa para los usuarios con el rol `auxiliar`.

### Fórmula de Haversine
Se calcula la distancia de círculo máximo entre la ubicación GPS del celular y el punto geográfico configurado en el sistema:

$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right)$$
$$c = 2 \cdot \operatorname{atan2}\left(\sqrt{a}, \sqrt{1-a}\right)$$
$$\text{Distancia} = R \cdot c$$

Donde $R = 6371000$ metros (radio de la Tierra).

### Lógica Implementada
1. Se verifica si el usuario pertenece al grupo `auxiliar`.
2. Se extrae `latitude` y `longitude` del cuerpo de la petición.
3. Se obtiene el registro de ubicación del sistema (`Ubicacion.objects.first()`). En su defecto, se aplica un centro y radio estándar.
4. Se calcula la distancia. Si supera el radio de geocerca, se lanza `AuthenticationFailed`.
5. Si la distancia es correcta, se comprueba si ya existe una asistencia para el día de hoy (`fecha = timezone.now().date()`). Si no existe, se crea el registro de check-in (`entrada = timezone.now().time()`).

## 3. Endpoints del API (`usuarios/auxiliar/`)

Se creó una nueva API para consultar el historial de asistencias de auxiliares.

### Serializador (`usuarios/auxiliar/serializers.py`)
```python
from rest_framework import serializers
from .models import Asistencia

class AsistenciaSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='id_user.username', read_only=True)
    first_name = serializers.CharField(source='id_user.first_name', read_only=True)
    last_name = serializers.CharField(source='id_user.last_name', read_only=True)

    class Meta:
        model = Asistencia
        fields = ['id', 'fecha', 'entrada', 'salida', 'id_user', 'username', 'first_name', 'last_name']
```

### Vista (`usuarios/auxiliar/views.py`)
```python
from rest_framework import viewsets, permissions
from .models import Asistencia
from .serializers import AsistenciaSerializer

class AsistenciaViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AsistenciaSerializer

    def get_queryset(self):
        queryset = Asistencia.objects.all().order_by('-fecha', '-entrada')
        user_id = self.request.query_params.get('user_id')
        if user_id:
            queryset = queryset.filter(id_user_id=user_id)
        return queryset
```

### Enrutamiento (`usuarios/auxiliar/urls.py`)
El ViewSet se expone bajo la ruta `/api/auxiliar/asistencias/`.
