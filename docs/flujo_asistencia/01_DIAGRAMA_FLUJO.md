# 01. Diagrama de Flujo de Asistencia por Geolocalización

Este documento describe el flujo completo desde que el auxiliar inicia sesión en la aplicación móvil hasta que se registra su asistencia en el servidor y se visualiza en la interfaz de administración web.

## 1. Diagrama de Flujo de Registro de Asistencia (Móvil → Servidor)

El siguiente diagrama detalla cómo se gestiona la geocerca durante el proceso de inicio de sesión:

```mermaid
sequenceDiagram
    autonumber
    actor Auxiliar as Auxiliar (App Móvil)
    participant Geolocator as Geolocator (GPS)
    participant AuthProvider as AuthProvider (Estado)
    participant Django as Servidor Backend
    database DB as Base de Datos

    Auxiliar->>Geolocator: Presiona "ENTRAR" (Pide permisos GPS)
    Geolocator-->>Auxiliar: Retorna latitud y longitud actuales
    Auxiliar->>AuthProvider: Solicita login con usuario, clave y coordenadas
    AuthProvider->>Django: POST /api/usuarios/login/ (JSON con coords)
    Django->>Django: Verifica credenciales (JWT)
    alt Credenciales incorrectas
        Django-->>AuthProvider: Error 401 (Contraseña incorrecta, etc.)
    else Credenciales válidas
        Django->>Django: ¿Es rol 'auxiliar'?
        alt No es auxiliar (Admin/Operador)
            Django-->>AuthProvider: Retorna Tokens JWT (Login exitoso)
        else Sí es auxiliar
            Django->>DB: Consulta ubicación del laboratorio (Ubicacion.objects.first())
            DB-->>Django: Coordenadas del laboratorio y radio de geocerca
            Django->>Django: Calcula distancia usando fórmula de Haversine
            alt Distancia > Radio (Fuera de rango)
                Django-->>AuthProvider: Error 401 (Fuera de rango permitido)
            else Distancia <= Radio (Dentro de rango)
                Django->>DB: ¿Ya tiene asistencia registrada hoy?
                alt No tiene asistencia hoy
                    Django->>DB: Registra Asistencia (fecha, entrada=hora_actual)
                end
                Django-->>AuthProvider: Retorna Tokens JWT (Login exitoso)
            end
        end
    end
    AuthProvider-->>Auxiliar: Navega a la pantalla de Inicio / Muestra error detallado
```

## 2. Diagrama de Flujo de Visualización de Asistencias (Web Admin)

```mermaid
sequenceDiagram
    autonumber
    actor Admin as Administrador (Web)
    participant page as page.tsx (Next.js)
    participant api as api/users.ts
    participant Django as Servidor Backend
    database DB as Base de Datos

    Admin->>page: Abre la sección de Gestión de Usuarios
    page->>page: Muestra pestañas (Administradores / Auxiliares y Operadores)
    Admin->>page: Selecciona pestaña "Auxiliares y Operadores"
    page->>page: Oculta columna de roles en la tabla
    Admin->>page: Hace clic en el botón "Asistencias" de un Auxiliar
    page->>api: Llama a fetchUserAttendances(userId)
    api->>Django: GET /api/auxiliar/asistencias/?user_id=ID
    Django->>DB: Consulta registros de asistencia ordenados por fecha y hora
    DB-->>Django: Lista de asistencias
    Django-->>api: Retorna JSON de asistencias
    api-->>page: Retorna datos de asistencias
    page->>page: Renderiza vista de historial "Auxiliar > Asistencias" con breadcrumb
    Admin->>page: Presiona el botón de retroceso (Flecha Izquierda)
    page->>page: Retorna a la lista principal de usuarios
```
