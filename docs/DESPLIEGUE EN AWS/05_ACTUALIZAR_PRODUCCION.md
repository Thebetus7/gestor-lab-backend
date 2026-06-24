# Paso 5: Actualizar el Proyecto en Producción

Cuando modificas código en tu PC y quieres que esos cambios se reflejen en AWS, el flujo es:

1. **Subes el código a GitHub** desde tu computadora.
2. **Entras al servidor AWS por SSH** y descargas ese código nuevo.
3. **Reconstruyes los contenedores Docker** para que usen el código actualizado.
4. **Ejecutas migraciones** si cambiaste la base de datos.

> **Importante:** Los pasos de la sección **A** los haces en tu PC. Los de la sección **B** los haces **dentro del servidor AWS**, después de conectarte por SSH.

---

## A) En tu PC local (antes de tocar el servidor)

Abre una terminal en la carpeta del proyecto backend en tu computadora:

```bash
cd gestor-lab-backend
```

Guarda tus cambios y súbelos a GitHub:

```bash
git add .
git commit -m "Descripción breve de lo que cambiaste"
git push origin main
```

**Qué hace cada comando:**
- `git add .` → marca todos los archivos modificados para subirlos.
- `git commit` → crea un "paquete" con esos cambios y un mensaje.
- `git push` → envía ese paquete a GitHub.

**Espera a que termine el push.** Solo cuando GitHub ya tenga el código nuevo, pasas al servidor.

---

## B) En el servidor AWS (paso a paso)

### B.1 — Conectarte al servidor por SSH

Desde **tu PC**, abre una terminal y conéctate a la EC2.

**En Windows (PowerShell):** ve a la carpeta donde guardaste el archivo `.pem`:

```powershell
cd C:\ruta\donde\guardaste\la\clave
ssh -i gestorlab-backend-key.pem ec2-user@TU_IP_PUBLICA_EC2
```

**En Linux/Mac:**

```bash
ssh -i gestorlab-backend-key.pem ec2-user@TU_IP_PUBLICA_EC2
```

Reemplaza `TU_IP_PUBLICA_EC2` por la IP que ves en la consola de AWS (ejemplo: `54.123.45.67`).

**Si la conexión es correcta**, verás un prompt como este:

```text
[ec2-user@ip-172-31-41-220 ~]$
```

Eso significa que **ya estás dentro del servidor**. Todo lo que escribas a partir de aquí se ejecuta en AWS, no en tu PC.

---

### B.2 — Ir a la carpeta del proyecto en el servidor

El repositorio se clonó en el primer despliegue. Entra a esa carpeta:

```bash
cd /home/ec2-user/gestor-lab-backend
```

**Verifica que estás en el lugar correcto:**

```bash
pwd
ls
```

**Qué deberías ver:**
- `pwd` debe mostrar: `/home/ec2-user/gestor-lab-backend`
- `ls` debe listar archivos como `docker-compose.yml`, `Dockerfile`, `manage.py`, `core/`, etc.

Si `ls` dice "No such file or directory", el proyecto no está ahí. Revisa si lo clonaste con otro nombre o en otra ruta.

---

### B.3 — Descargar el código nuevo desde GitHub

Con la carpeta correcta abierta, trae los cambios que subiste desde tu PC:

```bash
git pull origin main
```

**Qué hace:** compara el código del servidor con GitHub y actualiza los archivos locales del servidor.

**Salida esperada si todo va bien:**

```text
Updating abc1234..def5678
Fast-forward
 usuarios/views.py | 10 +++++-----
 1 file changed, 5 insertions(+), 5 deletions(-)
```

**Si Git dice** `Already up to date`, el servidor ya tenía la última versión (quizá el `git push` desde tu PC no se completó).

**Si Git pide usuario/contraseña** y falla, el repo puede ser privado. En ese caso configura acceso con token o SSH en el servidor (fuera del alcance de esta guía básica).

---

### B.4 — Reconstruir y reiniciar los contenedores

Sigue en la misma carpeta (`/home/ec2-user/gestor-lab-backend`).

**Antes de construir**, confirma que Buildx es compatible (evita el error `compose build requires buildx 0.17.0 or later`):

```bash
docker buildx version
```

Debe mostrar **0.17.0 o superior**. Si muestra `0.12.1`, aplica la [sección 3.2](./03_INSTALAR_HERRAMIENTAS.md#32--instalar-docker-buildx-obligatorio-en-amazon-linux-2023) o la solución de problemas antes de continuar.

Luego reconstruye y levanta los contenedores:

```bash
docker-compose up -d --build
```

**Qué hace cada parte:**
- `up` → levanta (o reinicia) los contenedores.
- `-d` → los deja corriendo en segundo plano (no bloquea la terminal).
- `--build` → **vuelve a construir la imagen** del backend con el código que acabas de bajar.

**Salida esperada si todo va bien:**

```text
[+] Building ...
[+] Running 2/2
 ✔ Container gestorlab_db       Running
 ✔ Container gestorlab_backend  Started
```

**Verifica que los contenedores están activos:**

```bash
docker-compose ps
```

Deberías ver `gestorlab_db` y `gestorlab_backend` con estado `Up`.

> **Nota:** Este comando **no borra la base de datos**. Los datos de PostgreSQL viven en un volumen Docker (`postgres_data`) y se conservan entre actualizaciones.

---

### B.5 — Aplicar migraciones y archivos estáticos (dentro del contenedor)

Estos comandos se ejecutan **dentro del contenedor `web`**, no directamente en el servidor. Docker los envía al contenedor de Django por ti.

**Siempre ejecuta `migrate`** después de actualizar (aunque no hayas tocado modelos, no hace daño):

```bash
docker-compose exec web python manage.py migrate
```

**Qué hace:** aplica cambios pendientes en la estructura de la base de datos (nuevas tablas, columnas, etc.).

**Recopila archivos estáticos** (CSS, JS admin, etc.):

```bash
docker-compose exec web python manage.py collectstatic --noinput
```

**Solo si agregaste o modificaste usuarios semilla**, ejecuta también:

```bash
docker-compose exec web python manage.py seed_users
```

| Comando | ¿Cuándo ejecutarlo? |
|---|---|
| `migrate` | **Siempre** después de cada actualización |
| `collectstatic` | **Siempre** después de cada actualización |
| `seed_users` | Solo si cambiaste `seed_users.py` o es un despliegue inicial |

---

### B.6 — Comprobar que la actualización funcionó

**1. Revisa los logs del backend** (busca errores):

```bash
docker-compose logs --tail=50 web
```

Si ves tracebacks de Python o errores de conexión a la BD, algo falló en el paso anterior.

**2. Prueba la API desde tu navegador o Postman:**

```text
http://TU_IP_PUBLICA_EC2/api/
```

**3. (Opcional) Verifica que responde desde el propio servidor:**

```bash
curl -I http://localhost/api/
```

Deberías recibir una respuesta HTTP (por ejemplo `200 OK` o `404` si no hay ruta raíz, pero **no** un error de conexión).

**4. Salir del servidor cuando termines:**

```bash
exit
```

Eso cierra la sesión SSH y vuelves a la terminal de tu PC.

---

### B.7 — Limpiar espacio en disco (opcional)

Cada `--build` deja imágenes Docker viejas ocupando espacio. En una EC2 pequeña (`t2.micro`) conviene limpiar de vez en cuando:

```bash
docker system prune -f
```

**Qué hace:** elimina imágenes y capas que ya no usa ningún contenedor. **No borra** el volumen de PostgreSQL ni los contenedores en ejecución.

---

## 📋 Resumen rápido (solo servidor AWS)

Copia y pega esto en orden **después de conectarte por SSH** y **después de haber hecho `git push` desde tu PC**:

```bash
cd /home/ec2-user/gestor-lab-backend
git pull origin main
docker buildx version
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic --noinput
docker-compose ps
docker-compose logs --tail=30 web
```

---

> **Siguiente paso:** [06_APAGAR_SERVICIOS.md](./06_APAGAR_SERVICIOS.md)  
> **Volver al índice:** [00_RESUMEN_GENERAL.md](./00_RESUMEN_GENERAL.md)
