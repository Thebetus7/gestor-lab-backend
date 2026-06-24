# Paso 1: Archivos de Configuración Requeridos en tu Proyecto

Para habilitar Docker en tu proyecto backend, debes asegurarte de tener los siguientes dos archivos en la raíz de tu carpeta `gestor-lab-backend/`:

### 📄 `Dockerfile`
Este archivo en la raíz del backend define cómo se construye la imagen de la aplicación:
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
Este archivo orquesta la aplicación web y la base de datos PostgreSQL:
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

> **Siguiente paso:** [02_CREAR_INSTANCIA_EC2.md](./02_CREAR_INSTANCIA_EC2.md)  
> **Volver al índice:** [00_RESUMEN_GENERAL.md](./00_RESUMEN_GENERAL.md)
