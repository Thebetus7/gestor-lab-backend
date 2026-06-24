# Paso 6: Apagar Servicios y Evitar Facturación en AWS

Si estás utilizando AWS para un proyecto académico o de prueba, es muy importante que sepas cómo apagar o eliminar los servicios cuando no los estés utilizando. AWS cobra por hora o segundo de uso, y dejar recursos encendidos de forma indefinida puede resultar en cobros inesperados.

En esta guía verás las opciones para pausar o eliminar por completo los servicios del Backend de GestorLab.

---

## 🔍 Opciones de Control de Costos

Dependiendo de si planeas retomar el proyecto pronto o si ya terminaste el trabajo por completo, tienes dos opciones principales en AWS EC2:

| Acción | ¿Qué pasa con los datos? | ¿Sigue cobrando AWS? | Ideal para... |
|---|---|---|---|
| **Detener Instancia (Stop)** | Se guarda todo el disco y la Base de Datos PostgreSQL. | **Casi nada.** No cobra por procesamiento (CPU/RAM), pero sí cobra una tarifa mínima por el almacenamiento en disco (EBS) y por IPs Elásticas sin usar. | Pausas cortas (ej. de un día para otro o durante el fin de semana). |
| **Terminar Instancia (Terminate)** | Se destruye la máquina virtual y su disco EBS. **Perderás tu base de datos.** | **$0 USD absolutos.** Se liberan todos los recursos asociados de forma definitiva. | Proyectos finalizados (ej. fin de ciclo académico o entrega final). |

---

## ⏸️ Opción 1: Detener la Instancia temporalmente (Stop)

Esta opción apaga la máquina virtual (como apagar tu computadora), pero mantiene intacto el disco duro (EBS). Cuando la vuelvas a encender, todo tu código, Docker, contenedores y la base de datos de PostgreSQL seguirán allí.

### Pasos en la Consola de AWS:
1. Inicia sesión en la **Consola de AWS** y ve al servicio **EC2**.
2. En el menú de la izquierda, haz clic en **"Instances"** (Instancias).
3. Selecciona tu instancia `gestorlab-backend-docker` marcando la casilla de verificación.
4. Haz clic en el botón superior **"Instance state"** (Estado de la instancia).
5. Selecciona **"Stop instance"** (Detener instancia).
6. Confirma haciendo clic en **"Stop"** cuando aparezca la advertencia.

> [!WARNING]
> Cuando detienes una instancia, su **IP pública dinámica cambiará** la próxima vez que la inicies. Tendrás que actualizar la IP del backend en la configuración de la Landing y usar la nueva IP para conectarte por SSH.

---

## 🗑️ Opción 2: Terminar la Instancia definitivamente (Terminate)

Esta opción elimina por completo la máquina virtual y su disco EBS. Úsala solo cuando ya no necesites el servidor en absoluto.

### Pasos en la Consola de AWS:
1. Ve al servicio **EC2** → **"Instances"**.
2. Selecciona la instancia `gestorlab-backend-docker`.
3. Haz clic en **"Instance state"** → **"Terminate instance"** (Terminar instancia).
4. Lee la advertencia y confirma haciendo clic en **"Terminate"**.

> [!CAUTION]
> Esta acción es irreversible. Se eliminará todo el contenido, **incluyendo los datos de los usuarios y laboratorios almacenados en PostgreSQL**. Asegúrate de haber realizado respaldos (dumps) si necesitas conservar la información.

---

## ⚠️ ¡Cuidado con los Costos Ocultos!

### 1. Direcciones IP Elásticas (Elastic IPs)
AWS no cobra por una IP Elástica **siempre y cuando** esté asociada a una instancia EC2 que esté **encendida**. Sin embargo, si detienes (Stop) o terminas (Terminate) la instancia, la IP Elástica queda "huérfana" y AWS te cobrará por cada hora que no se use para evitar el desperdicio de direcciones IP.

**Cómo liberarla:**
1. En la consola de EC2, ve a **"Network & Security"** → **"Elastic IPs"** (en el menú izquierdo).
2. Selecciona la IP elástica que creaste.
3. Haz clic en **"Actions"** → **"Disassociate Elastic IP address"** (Desasociar).
4. Luego, haz clic en **"Actions"** → **"Release Elastic IP address"** (Liberar).
5. Confirma la liberación. La IP desaparecerá de tu cuenta y no generará más cobros.

### 2. Volúmenes de Almacenamiento EBS (Discos virtuales)
Si utilizaste la **Opción 1 (Detener)**, el disco duro de 8 GiB sigue existiendo. AWS cobra aproximadamente $0.08 USD por GB al mes.
* Si terminas la instancia (Opción 2), el volumen EBS configurado para "eliminar al terminar" se borrará automáticamente.

---

## 🔄 Cómo Reactivar el Servicio después de un Stop

Si detuviste la instancia (Opción 1) y quieres volver a trabajar:

1. Ve a **EC2** → **"Instances"**.
2. Selecciona tu instancia `gestorlab-backend-docker`.
3. Haz clic en **"Instance state"** → **"Start instance"** (Iniciar instancia).
4. Espera a que el estado cambie a **"Running"** (Ejecutándose).
5. **Busca la nueva "Public IPv4 address"** en los detalles de la instancia (ya que cambió al encenderse).
6. Conéctate de nuevo por SSH usando la nueva IP:
   ```bash
   ssh -i gestorlab-backend-key.pem ec2-user@NUEVA_IP_PUBLICA
   ```
7. Los contenedores de Docker pueden estar apagados. Para levantarlos de nuevo, ve a la carpeta y ejecuta:
   ```bash
   cd /home/ec2-user/gestor-lab-backend
   docker-compose up -d
   ```
8. **Importante:** Como la IP pública cambió, recuerda **actualizar la configuración de tu frontend** (Landing) para que apunte a la nueva dirección del backend.

---

> **Volver al índice:** [00_RESUMEN_GENERAL.md](./00_RESUMEN_GENERAL.md)  
> **Paso anterior:** [05_ACTUALIZAR_PRODUCCION.md](./05_ACTUALIZAR_PRODUCCION.md)
