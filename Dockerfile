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