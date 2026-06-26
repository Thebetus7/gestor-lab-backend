# 04. Detalle Técnico: Frontend Web (Next.js)

Este documento detalla las modificaciones en el panel web de administración para la visualización del control de asistencia.

## 1. Conexión de API (`src/lib/api/users.ts`)

Se agregó la función para consumir el endpoint del historial de asistencia:
```typescript
export async function fetchUserAttendances(token: string, userId: number) {
  const res = await fetch(`${API_URL}/auxiliar/asistencias/?user_id=${userId}`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Accept': 'application/json',
    },
  });
  if (!res.ok) {
    throw new Error('Fallo al obtener el historial de asistencias');
  }
  return res.json();
}
```

## 2. Rediseño de Tabla (`src/app/usuarios/_components/UsersTable.tsx`)

Se removieron los elementos del rol debido a la nueva segmentación por pestañas:
1. **Remoción de Columna**: Se quitó la cabecera `<th>Roles</th>` y el correspondiente popover de filtros.
2. **Remoción de Celda**: Se eliminó la celda de la fila `<td>` que listaba los roles como Badges.
3. **Acción de Asistencias**: Se añadió un nuevo botón con estilo Material Design 3 en las filas de los usuarios con rol `auxiliar` para disparar el callback `onViewAttendances(u)`.

## 3. Segmentación por Pestañas (`src/app/usuarios/page.tsx`)

Se implementó un switch/controlador segmentado en la parte superior de la tabla con dos opciones:
- **Administradores**: Filtra la lista de usuarios mostrando únicamente aquellos que poseen el rol `'admin'`.
- **Auxiliares y Operadores**: Muestra aquellos usuarios que poseen el rol `'auxiliar'` u `'operador'`, o no tienen roles definidos.

Esto proporciona una división clara de responsabilidades y personal.

## 4. Vista de Historial de Asistencias (Sub-Página Reactiva)

Al hacer clic en "Asistencias" en la tabla, el componente `UsuariosPage` cambia de estado ocultando la tabla principal y renderizando la sub-vista de asistencia del auxiliar:
1. **Navegación / Breadcrumbs**: Visualización jerárquica clara (`Usuarios > Auxiliares > Asistencias`).
2. **Botón de Retroceso**: Un botón circular interactivo con icono de flecha hacia la izquierda que limpia el usuario seleccionado y regresa a la tabla.
3. **Tabla de Asistencias**:
   - Columnas: `Fecha`, `Hora de Entrada`, `Hora de Salida`, `Estado`.
   - Fecha formateada en español completo (Ej: *"viernes, 26 de junio de 2026"*).
   - Estado: `Completo` (si tiene entrada y salida registrada) o `Solo Entrada` (si la salida aún no se ha registrado).
   - Micro-estados de carga y vacíos personalizados.
