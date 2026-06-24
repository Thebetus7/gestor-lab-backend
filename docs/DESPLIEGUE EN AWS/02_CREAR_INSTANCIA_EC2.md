# Paso 2: Crear la Instancia EC2 en AWS

Sigue estos pasos en la consola de AWS para crear la máquina virtual que alojará el backend:

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
   - Permitir **HTTP** (puerto `80`) desde cualquier lugar (`0.0.0.0/0`) (ya que Docker Compose mapeará el puerto 80 del servidor directamente a la app Django).
   - Opcionalmente, permitir puerto **5432** si necesitas conectarte directamente a la base de datos PostgreSQL desde una herramienta externa.
6. **Almacenamiento:** `8 GiB gp3`.

---

> **Siguiente paso:** [03_INSTALAR_HERRAMIENTAS.md](./03_INSTALAR_HERRAMIENTAS.md)  
> **Volver al índice:** [00_RESUMEN_GENERAL.md](./00_RESUMEN_GENERAL.md)
