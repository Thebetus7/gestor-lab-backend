# Backend - GestorLab

Backend desarrollado en **Django 6.0**, implementando **Django REST Framework** para la creación de APIs y **SimpleJWT** para la autenticación sin estados basada en tokens (autenticación tipo Jetstream).

## Filosofía de Paquetería
- **Django**: Escalabilidad y solapamiento rápido de modelos de base de datos a APIs.
- **Django REST Framework (DRF)**: Construcción del API de forma moderna y estandarizada.
- **djangorestframework-simplejwt**: Paquete preferido cuando no se usa el sistema de plantillas clásico. Permite crear tokens firmados y autorizar componentes remotos (Next.js y Flutter).
- **Grupos y Permisos**: El usuario `CustomUser` es extendido y mapea los roles (estilo Spatie) directamente con los "Grupos" estándar de Django, una solución nativa y que no requiere dependencias pesadas extras.
- **python-dotenv**: Permite leer configuraciones desde `.env` para facilitar el uso en diferentes entornos.

## Credenciales Semilla (Variables Fijas de Ejemplo)
Una vez conectada la base de datos de Postgres y corridas las migraciones (`python manage.py migrate`), se deben popular los usuarios y roles corriendo el comando personalizado:

```bash
python manage.py seed_users
```

**Usuarios iniciales precargados:**

1. **Usuario Administrador:**
   - **Usuario**: `admin_test`
   - **Contraseña**: `Admin1234!`
   - **Rol**: `admin`

2. **Usuario Operador:**
   - **Usuario**: `operador_test`
   - **Contraseña**: `Operador1234!`
   - **Rol**: `operador`
