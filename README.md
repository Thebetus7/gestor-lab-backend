# Backend - GestorLab

Backend desarrollado en **Django 6.0**, implementando **Django REST Framework** para la creación de APIs y **SimpleJWT** para la autenticación sin estados basada en tokens (autenticación tipo Jetstream).

## Filosofía de Paquetería
- **Django**: Escalabilidad y solapamiento rápido de modelos de base de datos a APIs.
- **Django REST Framework (DRF)**: Construcción del API de forma moderna y estandarizada.
- **djangorestframework-simplejwt**: Paquete preferido cuando no se usa el sistema de plantillas clásico. Permite crear tokens firmados y autorizar componentes remotos (Next.js y Flutter).
- **Grupos y Permisos**: El usuario `CustomUser` es extendido y mapea los roles (estilo Spatie) directamente con los "Grupos" estándar de Django, una solución nativa y que no requiere dependencias pesadas extras.
- **python-dotenv**: Permite leer configuraciones desde `.env` para facilitar el uso en diferentes entornos.

## Guía de Instalación y Configuración

Sigue estos pasos para configurar el entorno de desarrollo localmente.

### 1. Preparar el Entorno Virtual (venv)
Es fundamental aislar las dependencias del proyecto.

```powershell
# Crear el entorno virtual
python -m venv venv

# Activar el entorno virtual (Windows)
.\venv\Scripts\activate
```
en bash:
```bash
source [backend]/venv/Scripts/activate
```

### 2. Instalar Dependencias
Una vez activado el entorno, instala los paquetes necesarios:

```powershell
pip install -r requirements.txt
```

### 3. Configuración del Entorno (.env)
Asegúrate de configurar tu archivo `.env` en la raíz del proyecto con las credenciales de PostgreSQL y la `SECRET_KEY` de Django.

### 4. Inicializar la Base de Datos
Aplica las migraciones para crear la estructura de tablas y luego ejecuta el seeder para los usuarios base:

```powershell
# Aplicar migraciones
python manage.py migrate

# Poblar base de datos con usuarios y roles iniciales
python manage.py seed_users
```

### 5. Levantar el Servidor de Desarrollo
Inicia el servidor para comenzar a recibir peticiones:

```powershell
python manage.py runserver
```
El API estará disponible en `http://127.0.0.1:8000/`.

## Manejo de la Base de Datos (Reset)

Para realizar un "Reset Total" (equivalente a un fresh en Laravel) y limpiar todo el esquema de PostgreSQL, ejecuta la siguiente secuencia de comandos:

```powershell
# 1. Ejecutar el script para limpiar el esquema de la base de datos
python reset_db.py

# 2. Recrear los archivos de migración (detectará todas las sub-apps)
python manage.py makemigrations

# 3. Aplicar las nuevas migraciones a la base de datos limpia
python manage.py migrate
```

Si necesitas reiniciar la base de datos por completo (pasos detallados), sigue estos pasos para asegurar una limpieza total:

### 1. Limpieza de Migraciones (Opcional)
Si has realizado cambios estructurales profundos y quieres que el historial de migraciones sea "limpio", puedes borrar los archivos de migración previos. 

**En Windows (PowerShell):**
```powershell
# Borra todos los archivos de migraciones generados (excepto los __init__.py)
Get-ChildItem -Path "**/migrations/*.py" -Exclude "__init__.py" | Remove-Item
```

### 2. Reiniciar el Esquema en PostgreSQL
Para borrar todas las tablas de forma rápida, puedes resetear el esquema `public`. Abre tu terminal de PostgreSQL (`psql`) o tu herramienta gráfica (pgAdmin) y ejecuta:

```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

### 3. Regenerar y Aplicar
Una vez limpia la base de datos, vuelve a generar la estructura:

```powershell
# Detectar cambios y crear archivos de migración
python manage.py makemigrations

# Crear las tablas en la base de datos
python manage.py migrate

# Volver a cargar los usuarios base
python manage.py seed_users
```

## Credenciales Semilla (Variables Fijas de Ejemplo)
Una vez conectada la base de datos de Postgres y corridas las migraciones, se deben popular los usuarios y roles corriendo el comando personalizado mencionado arriba:

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
