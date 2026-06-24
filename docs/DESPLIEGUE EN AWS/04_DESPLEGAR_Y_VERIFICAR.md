# Paso 4: Subir y Desplegar el Proyecto en AWS

Una vez preparadas las herramientas en el servidor, desplegaremos la aplicación y la base de datos PostgreSQL.

## 4.1 Clonar el proyecto
Clona tu repositorio en la EC2:
```bash
git clone <URL_DEL_REPOSITORIO> gestor-lab-backend
cd gestor-lab-backend
```

## 4.2 Confirmar versión de Buildx
**Confirma que Buildx está listo** (solo la primera vez o si ves el error de buildx):
```bash
docker buildx version
```
Debe mostrar `v0.17.0` o superior. Si no, vuelve al paso anterior de instalación.

## 4.3 Levantar contenedores
Levanta los contenedores en segundo plano (background):
```bash
docker-compose up -d --build
```

## 4.4 Configurar base de datos (Migraciones)
Ejecuta las migraciones, carga los usuarios semilla y recopila estáticos dentro del contenedor de Django:
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

**Qué significa:** Docker Compose intentó **construir la imagen** del backend (`build: .` en `docker-compose.yml`), pero Buildx no cumple el mínimo requerido (**0.17.0**). En Amazon Linux 2023 es muy común tener **0.12.1** por defecto.

**Causa habitual en Amazon Linux 2023:**
- `sudo dnf install docker-buildx-plugin` → falla con `No match for argument`
- `docker buildx version` → muestra `0.12.1`

**Solución** (ejecuta en la EC2):

```bash
# 1. Instalar Buildx actualizado manualmente
sudo mkdir -p /usr/local/lib/docker/cli-plugins
sudo curl -L "https://github.com/docker/buildx/releases/download/v0.19.3/buildx-v0.19.3.linux-amd64" \
  -o /usr/local/lib/docker/cli-plugins/docker-buildx
sudo chmod +x /usr/local/lib/docker/cli-plugins/docker-buildx

# 2. Verificar versión (debe ser >= 0.17.0)
docker buildx version

# 3. Si sigue en 0.12.1, forzar el plugin nuevo
export DOCKER_CLI_PLUGIN_EXTRA_DIRS=/usr/local/lib/docker/cli-plugins
echo 'export DOCKER_CLI_PLUGIN_EXTRA_DIRS=/usr/local/lib/docker/cli-plugins' >> ~/.bashrc
docker buildx version

# 4. Reiniciar Docker y reintentar despliegue
sudo systemctl restart docker
cd ~/gestor-lab-backend
docker-compose up -d --build
```

**Plan B** (si Compose sigue fallando al build):

```bash
cd ~/gestor-lab-backend
docker build -t gestor-lab-backend-web .
docker-compose up -d
docker-compose ps
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

> **Siguiente paso:** [05_ACTUALIZAR_PRODUCCION.md](./05_ACTUALIZAR_PRODUCCION.md)  
> **Volver al índice:** [00_RESUMEN_GENERAL.md](./00_RESUMEN_GENERAL.md)
