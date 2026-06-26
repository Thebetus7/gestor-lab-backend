# 03. Detalle Técnico: Aplicación Móvil (Flutter)

Este documento describe la integración y los cambios realizados en la aplicación móvil **gestor_lab_movil**.

## 1. Dependencias Instaladas (`pubspec.yaml`)

Se añadieron paquetes necesarios para la geolocalización y renderizado de mapas nativos/OSM sin dependencias externas complejas:
- `geolocator: ^14.0.3` (para solicitar permisos y consultar coordenadas de alta precisión).
- `flutter_map: ^8.3.0` (visualizador interactivo de mapas basado en OpenStreetMap).
- `latlong2: ^0.9.1` (estructura de coordenadas Lat/Lng).

## 2. Permisos del Dispositivo

### Android (`android/app/src/main/AndroidManifest.xml`)
Se añadieron las líneas de permisos en el nodo manifest principal:
```xml
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
```

### iOS (`ios/Runner/Info.plist`)
Se configuraron las claves explicativas que se le mostrarán al usuario al solicitar permisos de geolocalización:
```xml
<key>NSLocationWhenInUseUsageDescription</key>
<string>Esta aplicación requiere acceso a su ubicación para registrar su asistencia al ingresar al laboratorio.</string>
<key>NSLocationAlwaysAndWhenInUseUsageDescription</key>
<string>Esta aplicación requiere acceso a su ubicación para registrar su asistencia al ingresar al laboratorio.</string>
```

## 3. Propagación de Parámetros en el Login

- **`AuthApi.login`**: Ahora agrega opcionalmente `latitude` y `longitude` en el cuerpo de la petición.
- **`AuthService.login`** & **`AuthRepository.login`**: Reciben los parámetros opcionales y los delegan.
- **`AuthProvider.login`**:
  - Llama al repositorio con la ubicación del GPS.
  - Se modificó la captura de errores en el bloque `catch` para extraer y parsear los mensajes descriptivos del backend (por ejemplo: `"Usted se encuentra fuera del rango permitido..."` en lugar del genérico `"Error de login. Revise sus credenciales."`).

## 4. Obtención Automática de Ubicación en el Login (`login_page.dart`)

Al presionar el botón **ENTRAR**, antes de invocar el flujo de autenticación, la aplicación intenta obtener la ubicación GPS actual si los servicios están activos y se han concedido los permisos:
```dart
double? latitude;
double? longitude;
try {
  bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
  if (serviceEnabled) {
    LocationPermission permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
    }
    if (permission == LocationPermission.always || permission == LocationPermission.whileInUse) {
      final position = await Geolocator.getCurrentPosition(
        desiredAccuracy: LocationAccuracy.high,
        timeLimit: const Duration(seconds: 5),
      );
      latitude = position.latitude;
      longitude = position.longitude;
    }
  }
} catch (_) {}
```

## 5. Pantalla de Mapa de Prueba (`gps_map_page.dart`)

Se añadió el botón **VER MAPA GPS (PRUEBA)** en la pantalla de login. Permite a los desarrolladores y usuarios verificar dónde está apuntando el GPS del dispositivo antes de loguearse:
- Renderiza la ubicación actual con un marcador de pin azul.
- Centra dinámicamente el mapa en las coordenadas Lat/Lng devueltas por el dispositivo.
