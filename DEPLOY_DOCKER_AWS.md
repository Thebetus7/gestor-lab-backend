# Despliegue Backend (Django + PostgreSQL) en AWS - CON DOCKER

Esta guía describe cómo empaquetar y desplegar el backend de **GestorLab** en AWS usando **Docker** y **Docker Compose**. Este enfoque aislará la aplicación y la base de datos PostgreSQL en contenedores independientes de forma limpia.

---

## 1. Archivos de Configuración Requeridos en tu Proyecto

Para habilitar Docker en tu proyecto backend, debes crear los siguientes dos archivos en la raíz de tu carpeta `gestor-lab-backend/`:

### 📄 `Dockerfile`
Crea este archivo en la raíz del backend:
```dockerfile
FROM python:3.11-slim

# Evitar que Python escriba archivos .pyc y forzar salida de logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias para compilar psycopg2 (controlador PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Instalar dependencias del proyecto
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn

# Copiar el código del proyecto
COPY . /app/

# Exponer el puerto de Django/Gunicorn
EXPOSE 8000

# Comando para correr en producción
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
```

### 📄 `docker-compose.yml`
Crea este archivo en la raíz del backend para orquestar la app y la base de datos PostgreSQL:
```yaml
services:
  db:
    image: postgres:15-alpine
    container_name: gestorlab_db
    restart: always
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_DB=SW2_GestorLab_1_26
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=123456789
    ports:
      - "5432:5432"

  web:
    build: .
    container_name: gestorlab_backend
    restart: always
    command: gunicorn --bind 0.0.0.0:8000 core.wsgi:application
    volumes:
      - .:/app
    ports:
      - "80:8000"  # Expone el puerto 80 del servidor hacia el 8000 del contenedor
    environment:
      - DEBUG=False
      - SECRET_KEY=TU_LLAVE_SECRETA_SUPER_SEGURA_PROD
      - DB_NAME=SW2_GestorLab_1_26
      - DB_USER=postgres
      - DB_PASSWORD=123456789
      - DB_HOST=db  # Apunta al nombre del servicio de la BD
      - DB_PORT=5432
    depends_on:
      - db

volumes:
  postgres_data:
```

---

## 2. Crear la Instancia EC2 en AWS

1. **Nombre:** `gestorlab-backend-docker`
2. **AMI:** **Amazon Linux 2023 AMI** (capa gratuita).
3. **Tipo de Instancia:** `t2.micro` o `t3.micro`.
4. **Par de claves (inicio de sesión - SSH):**
   * Haz clic en **"Crear un nuevo par de claves"** (si no tienes una).
   * Llámalo `gestorlab-backend-key`.
   * Tipo de clave: **RSA**. Formato de archivo: **`.pem`**.
   * Presiona **Crear**. Tu navegador descargará automáticamente el archivo `gestorlab-backend-key.pem`. **Guárdalo en un lugar seguro**, ya que lo usarás para conectarte por SSH.
5. **Configuraciones de red (Security Group):**
   - Permitir **SSH** (puerto `22`) desde cualquier lugar (`0.0.0.0/0`).
   - Permitir **HTTP** (puerto `80`) desde cualquier lugar (`0.0.0.0/0`) (ya que Docker Compose mapeará el puerto 80 del servidor directamente a la app).
5. **Almacenamiento:** `8 GiB gp3`.

---

## 3. Instalar Docker y Docker Compose en la EC2

Conéctate por SSH a la EC2 y ejecuta:

```bash
# Actualizar el sistema
sudo dnf update -y

# Instalar Docker, Buildx (requerido para compilar imágenes) y Git
sudo dnf install docker docker-buildx-plugin git -y

# Iniciar e instalar el servicio de Docker al arranque
sudo systemctl start docker
sudo systemctl enable docker

# Agregar tu usuario al grupo docker (para no usar sudo en cada comando)
sudo usermod -aG docker ec2-user
```
> [!IMPORTANT]
> Para aplicar el cambio de grupo de Docker puedes:
> 1. Cerrar la conexión SSH actual ejecutando `exit` y conectarte de nuevo.
> 2. **O ejecutar en la terminal activa:** `newgrp docker` (esto aplicará los permisos de forma inmediata en la sesión actual).

### Instalar Docker Compose:
```bash
# Descargar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Asignar permisos de ejecución
sudo chmod +x /usr/local/bin/docker-compose

# Verificar versiones
docker-compose --version
docker buildx version
```

> Si `docker buildx version` falla o muestra una versión menor a `0.17.0`, instala Buildx manualmente:
> ```bash
> sudo mkdir -p /usr/local/lib/docker/cli-plugins
> sudo curl -L "https://github.com/docker/buildx/releases/download/v0.19.3/buildx-v0.19.3.linux-amd64" \
>   -o /usr/local/lib/docker/cli-plugins/docker-buildx
> sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx
> docker buildx version
> ```

---

## 4. Subir y Desplegar el Proyecto en AWS

1. Clona tu repositorio en la EC2:
   ```bash
   git clone <URL_DEL_REPOSITORIO> gestor-lab-backend
   cd gestor-lab-backend
   ```
2. Levanta los contenedores en segundo plano (background):
   ```bash
   docker-compose up -d --build
   ```
3. Ejecuta las migraciones, carga los usuarios semilla y recopila estáticos dentro del contenedor de Django:
   ```bash
   # Correr migraciones de base de datos
   docker-compose exec web python manage.py migrate
   
   # Crear usuarios y roles iniciales (admin, operador, auxiliares)
   docker-compose exec web python manage.py seed_users
   
   # Recopilar archivos estáticos
   docker-compose exec web python manage.py collectstatic --noinput
   ```

   > **Nota:** El comando `seed_users` (`usuarios/autenticacion/management/commands/seed_users.py`) es **obligatorio** en el primer despliegue. Crea los grupos `admin`, `operador` y `auxiliar`, y los usuarios iniciales del sistema (`admin`, `operador_test`, `auxBeto`, `auxJuan`). Si ya existen, actualiza sus credenciales sin duplicarlos.

¡Listo! Tu backend está en línea en `http://IP_PUBLICA_EC2/api`.

---

## ⚠️ Solución de problemas

### `compose build requires buildx 0.17.0 or later`

**Qué significa:** Docker Compose intentó **construir la imagen** de tu backend (`build: .` en `docker-compose.yml`), pero el servidor no tiene **Docker Buildx** instalado o la versión es muy antigua. Sin Buildx, el build no puede continuar y los contenedores no se levantan.

**Cómo solucionarlo** (ejecuta en la EC2):

```bash
# Opción A: paquete de Amazon Linux (recomendado)
sudo dnf install docker-buildx-plugin -y

# Opción B: si la opción A no funciona, instalar Buildx manualmente
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -L "https://github.com/docker/buildx/releases/download/v0.19.3/buildx-v0.19.3.linux-amd64" \
  -o /usr/local/lib/docker/cli-plugins/docker-buildx
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

# Verificar que Buildx quedó instalado (debe mostrar v0.17.0 o superior)
docker buildx version

# Volver a intentar el despliegue
cd ~/gestor-lab-backend
docker-compose up -d --build
```

### `the attribute version is obsolete`

**Qué significa:** Es solo una **advertencia**, no un error. Las versiones nuevas de Docker Compose ya no usan la línea `version: '3.8'` al inicio del archivo. Puedes ignorarla o eliminar esa línea de `docker-compose.yml`.

---

## 🛑 Comandos de Mantenimiento

### Ver Logs:
```bash
docker-compose logs -f web
```

### Detener los Contenedores:
```bash
docker-compose down
```

### Reiniciar/Levantar de nuevo:
```bash
docker-compose up -d
```

---

## 🔄 Actualizar el Proyecto en Producción (Desplegar Nuevos Cambios)

Con Docker, actualizar tu aplicación en producción se reduce a reconstruir los contenedores:

1. **Subir los cambios a tu repositorio Git (En tu PC local):**
   ```bash
   git add .
   git commit -m "Actualización de backend con Docker"
   git push origin main
   ```

2. **Descargar los cambios y recompilar (En el Servidor AWS por SSH):**
   Conéctate al servidor, navega a la carpeta y haz pull de los cambios:
   ```bash
   cd /home/ec2-user/gestor-lab-backend
   git pull origin main
   ```

3. **Reconstruir y levantar los contenedores (En el Servidor AWS):**
   Usa Docker Compose para reconstruir la imagen web con el nuevo código y levantar la app sin borrar el volumen de base de datos PostgreSQL:
   ```bash
   docker-compose up -d --build
   ```

4. **Correr migraciones dentro del contenedor (En el Servidor AWS):**
   Si modificaste modelos de datos en Django (`models.py`), ejecuta las migraciones correspondientes dentro del contenedor levantado:
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py collectstatic --noinput
   ```

5. **Limpiar imágenes obsoletas para liberar espacio (Opcional):**
   Compilar nuevas imágenes deja imágenes viejas "huérfanas" en el disco de la EC2. Libera espacio ejecutando:
   ```bash
   docker system prune -f
   ```
