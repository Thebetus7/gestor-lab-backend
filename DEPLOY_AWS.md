# Despliegue Backend (Django + PostgreSQL) en AWS - SIN DOCKER (Vanilla)

Esta guía describe paso a paso cómo desplegar el backend de **GestorLab** directamente sobre el sistema operativo de una instancia EC2 en AWS utilizando **Amazon Linux 2023** y una base de datos **PostgreSQL** local.

---

## 1. Crear el Servidor EC2 (Consola de AWS)

1. **Nombre:** `gestorlab-backend`
2. **Sistema Operativo (AMI):** **Amazon Linux 2023 AMI** (elegible para capa gratuita).
3. **Tipo de Instancia:** `t2.micro` o `t3.micro`.
4. **Par de claves (SSH):** Crea o selecciona una clave `.pem` (ej. `gestorlab-backend-key.pem`).
5. **Configuración de Red (Security Group):**
   - Permitir tráfico **SSH** desde cualquier lugar (`0.0.0.0/0`) o desde tu IP.
   - Permitir tráfico **HTTP** (puerto `80`) desde cualquier lugar (`0.0.0.0/0`) (Nginx actuará como proxy inverso).
   - *(Opcional)* Si deseas conectarte directamente a Django sin Nginx para pruebas: agrega una regla para el puerto `8000` (TCP personalizado).
6. **Almacenamiento:** `8 GiB gp3` (por defecto).

---

## 2. Conexión SSH al Servidor (Desde tu PC Local)

Abre una terminal Git Bash (o similar) en la carpeta donde guardaste tu llave `.pem` y ejecuta:

```bash
# Asignar permisos correctos a la llave
chmod 400 gestorlab-backend-key.pem

# Conectarse a la instancia
ssh -i gestorlab-backend-key.pem ec2-user@IP_PUBLICA_EC2
```

---

## 3. Instalar Dependencias del Sistema y Python

Una vez dentro de la máquina de AWS, ejecuta los siguientes comandos para actualizar e instalar las dependencias básicas:

```bash
# Actualizar gestor de paquetes
sudo dnf update -y

# Instalar Python 3.11, pip y herramientas de desarrollo para PostgreSQL
sudo dnf install python3.11 python3.11-pip python3.11-devel postgresql15-devel gcc git -y
```

---

## 4. Instalar y Configurar la Base de Datos PostgreSQL

Instalaremos PostgreSQL 15 directamente en la máquina EC2:

```bash
# Instalar servidor de PostgreSQL
sudo dnf install postgresql15-server -y

# Inicializar la base de datos
sudo postgresql-setup --initdb

# Habilitar e iniciar el servicio
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### Crear la base de datos y usuario:
1. Conéctate a la consola interactiva de PostgreSQL:
   ```bash
   sudo -i -u postgres psql
   ```
2. Ejecuta los comandos SQL para crear la base de datos según tu configuración de `.env`:
   ```sql
   CREATE DATABASE "SW2_GestorLab_1_26";
   CREATE USER postgres WITH PASSWORD '123456789';
   GRANT ALL PRIVILEGES ON DATABASE "SW2_GestorLab_1_26" TO postgres;
   \q
   ```

3. Modifica la configuración de autenticación para permitir conexiones locales mediante contraseña. Abre el archivo de configuración:
   ```bash
   sudo nano /var/lib/pgsql/data/pg_hba.conf
   ```
   Busca las líneas al final del archivo y cambia el método `peer` e `ident` por **`md5`** o **`trust`** para conexiones locales:
   ```text
   # TYPE  DATABASE        USER            ADDRESS                 METHOD
   local   all             all                                     md5
   host    all             all             127.0.0.1/32            md5
   host    all             all             ::1/128                 md5
   ```
   *(Guarda los cambios con Ctrl+O, Enter y sal con Ctrl+X).*

4. Reinicia PostgreSQL:
   ```bash
   sudo systemctl restart postgresql
   ```

---

## 5. Subir y Configurar el Proyecto

1. Clona tu repositorio de Git en la carpeta `/home/ec2-user/` o transfiere el código usando SCP.
   ```bash
   git clone <URL_DE_TU_REPOSITORIO> gestor-lab-backend
   cd gestor-lab-backend
   ```
2. Crea el entorno virtual e instala los requerimientos:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install gunicorn  # Necesario para producción
   ```

3. Configura el archivo de entorno `.env` en producción:
   ```bash
   nano .env
   ```
   Agrega las variables para producción (modificando el `DEBUG` a `False`):
   ```env
   DEBUG=False
   SECRET_KEY=TU_LLAVE_SECRETA_SUPER_SEGURA_PROD
   DB_NAME=SW2_GestorLab_1_26
   DB_USER=postgres
   DB_PASSWORD=123456789
   DB_HOST=localhost
   DB_PORT=5432
   ```

4. Ejecuta migraciones, crea el superusuario y recopila estáticos:
   ```bash
   python manage.py migrate
   python manage.py collectstatic --noinput
   
   # Opcional: Ejecutar scripts iniciales
   python reset_db.py
   python manage.py createsuperuser
   ```

---

## 6. Configurar Gunicorn y Systemd (Servicio en Segundo Plano)

Crearemos un servicio de systemd para que Django corra automáticamente en el fondo y se reinicie ante fallas.

1. Crea el archivo del servicio:
   ```bash
   sudo nano /etc/systemd/system/gestorlab-backend.service
   ```
2. Pega el siguiente contenido (asegúrate de que los paths coincidan con tu ruta):
   ```ini
   [Unit]
   Description=GestorLab Django Backend Daemon
   After=network.target postgresql.service

   [Service]
   User=ec2-user
   WorkingDirectory=/home/ec2-user/gestor-lab-backend
   ExecStart=/home/ec2-user/gestor-lab-backend/venv/bin/gunicorn \
             --workers 3 \
             --bind 127.0.0.1:8000 \
             core.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
3. Inicia y habilita el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start gestorlab-backend
   sudo systemctl enable gestorlab-backend
   ```

---

## 7. Configurar Nginx como Proxy Inverso (Puerto 80)

Instalaremos Nginx para escuchar en el puerto `80` y redirigir el tráfico a Gunicorn en el puerto `8000`.

1. Instala Nginx:
   ```bash
   sudo dnf install nginx -y
   ```
2. Edita la configuración principal de Nginx:
   ```bash
   sudo nano /etc/nginx/nginx.conf
   ```
3. Busca el bloque `server` dentro de `http` y configúralo para redirigir las peticiones y servir los archivos estáticos de Django:
   ```nginx
   server {
       listen       80;
       listen       [::]:80;
       server_name  _;

       # Archivos estáticos de Django
       location /static/ {
           alias /home/ec2-user/gestor-lab-backend/static/;
       }

       # Proxy a Gunicorn
       location / {
           proxy_set_header Host $http_host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_pass http://127.0.0.1:8000;
       }
   }
   ```
4. Dale permisos de lectura a Nginx sobre el directorio de usuario (necesario para leer archivos estáticos en `/home/ec2-user`):
   ```bash
   chmod 711 /home/ec2-user
   chmod -R 755 /home/ec2-user/gestor-lab-backend
   ```
5. Inicia y habilita Nginx:
   ```bash
   sudo systemctl restart nginx
   sudo systemctl enable nginx
   ```

Tu backend ahora está desplegado y accesible públicamente en `http://IP_PUBLICA_EC2/api`.

---

## 🛑 Apagar / Iniciar Servicios para Ahorrar Costos

### Detener Temporalmente Django y Nginx (La máquina sigue encendida):
```bash
sudo systemctl stop nginx
sudo systemctl stop gestorlab-backend
```

### Detener la Instancia EC2 completa (Recomendado):
Entra a la Consola de AWS -> EC2 -> Instancias -> Selecciona tu instancia -> **Detener instancia**. 
*Nota: Al reiniciar la máquina, la IP pública cambiará. Debes actualizar la variable `NEXT_PUBLIC_API_URL` en el frontend y compilarlo nuevamente.*

---

## 🔄 Actualizar el Proyecto en Producción (Desplegar Nuevos Cambios)

Si realizaste cambios en tu código localmente (nuevas vistas, arreglaste errores, etc.) y deseas subirlos al servidor AWS:

1. **Subir los cambios a tu repositorio Git (En tu PC local):**
   ```bash
   git add .
   git commit -m "Actualización de backend"
   git push origin main
   ```

2. **Descargar los cambios en la máquina de AWS (En el Servidor AWS por SSH):**
   Conéctate por SSH al servidor, navega a la carpeta del proyecto y haz pull:
   ```bash
   cd /home/ec2-user/gestor-lab-backend
   git pull origin main
   ```

3. **Instalar dependencias y migrar base de datos (En el Servidor AWS):**
   Activa tu entorno virtual y ejecuta las instalaciones o migraciones si es que modificaste modelos de base de datos (`models.py`) o requerimientos:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```

4. **Reiniciar los servicios para aplicar cambios (En el Servidor AWS):**
   Reinicia el demonio de Gunicorn para que cargue la versión actualizada de tu código de Python:
   ```bash
   sudo systemctl restart gestorlab-backend
   ```
