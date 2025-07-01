# Sistema de Monitoreo de Pacientes - API

## 🏥 Descripción

API completa desarrollada con **FastAPI** para el monitoreo de signos vitales de pacientes en tiempo real. El sistema simula datos de sensores médicos y está preparado para integración con dispositivos **ESP32** y sensores reales.

## 🚀 Características

- **API RESTful** completa con FastAPI
- **Simulación de datos** realistas de signos vitales
- **Base de datos MySQL** con estructura optimizada
- **Generación automática** de datos cada 30 segundos
- **Sistema de alertas** por colores (verde, amarilla, roja)
- **Predicciones de IA** simuladas
- **Preparado para MQTT** y ESP32
- **Documentación interactiva** con Swagger
- **CORS habilitado** para apps web y móviles
- **Docker Compose** para deployment fácil

## 📊 Endpoints Principales

### Pacientes
- `GET /pacientes/` - Lista todos los pacientes
- `POST /pacientes/` - Crear nuevo paciente
- `GET /pacientes/{id}` - Obtener paciente específico

### Mediciones
- `GET /mediciones/` - Obtener mediciones con filtros
- `POST /mediciones/` - Crear nueva medición
- `GET /mediciones/tiempo-real/{id}` - Datos en tiempo real

### Alertas
- `GET /alertas/` - Obtener alertas con filtros
- `GET /alertas/criticas` - Alertas críticas recientes

### Predicciones
- `GET /predicciones/` - Obtener predicciones
- `POST /predicciones/generar/{id}` - Generar nueva predicción

### Estadísticas
- `GET /estadisticas/dashboard/{id}` - Dashboard completo del paciente

## 🛠️ Instalación

### Opción 1: Instalación Local

1. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

2. **Configurar MySQL**:
- Crear la base de datos usando el script SQL proporcionado
- Ajustar la cadena de conexión en `database.py` si es necesario

3. **Ejecutar la aplicación**:
```bash
python run_server.py
```

### Opción 2: Docker Compose (Recomendado)

```bash
# Clonar el proyecto
git clone https://github.com/h-marshall69/fastapi_app
cd fastapi_app

# Ejecutar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f api
```

## 📋 Uso

### 1. Generar Datos de Prueba

```bash
# Ejecutar script de prueba
python test_api.py

# O usar el endpoint directamente
curl -X POST http://localhost:8000/utilidad/generar-datos-prueba
```

### 2. Acceder a la Documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Ejemplos de Uso

```python
import requests

# Obtener pacientes
response = requests.get("http://localhost:8000/pacientes/")
pacientes = response.json()

# Obtener mediciones en tiempo real
patient_id = 1
response = requests.get(f"http://localhost:8000/mediciones/tiempo-real/{patient_id}")
data = response.json()

# Crear nueva medición
nueva_medicion = {
    "id_paciente": 1,
    "bpm": 75,
    "spo2": 98.2,
    "temperatura": 36.8
}
response = requests.post("http://localhost:8000/mediciones/", json=nueva_medicion)
```

## 🔧 Estructura del Proyecto

```
├── main.py              # Aplicación principal FastAPI
├── database.py          # Configuración de base de datos
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Esquemas Pydantic
├── services.py          # Lógica de negocio
├── mqtt_handler.py      # Preparado para MQTT/ESP32
├── run_server.py        # Script para ejecutar servidor
├── test_api.py          # Script de pruebas
├── requirements.txt     # Dependencias Python
├── docker-compose.yml   # Configuración Docker
├── Dockerfile          # Imagen Docker
└── README.md           # Documentación
```

## 🔌 Integración con ESP32

El sistema está preparado para recibir datos del ESP32 vía MQTT:

### Formato de datos esperado:
```json
{
    "patient_id": 1,
    "bpm": 75,
    "spo2": 98.5,
    "body_temp": 36.8,
    "ambient_temp": 22.5,
    "timestamp": "2024-01-15T10:30:00"
}
```

### Configuración ESP32:
- **Broker MQTT**: localhost:1883
- **Tópico**: `esp32/sensors/{patient_id}/data`
- **Formato**: JSON

## 🚨 Sistema de Alertas

### Alertas Críticas (Rojas):
- BPM > 120 o < 50
- SpO2 < 90%
- Temperatura > 39°C o < 35°C

### Alertas de Precaución (Amarillas):
- BPM > 100 o < 60
- SpO2 < 95%
- Temperatura > 37.5°C o < 36°C

## 🤖 Predicciones de IA

El sistema incluye predicciones simuladas para:
- Hipertensión
- Diabetes Tipo 2
- Arritmia Cardíaca
- Anemia
- Hipotiroidismo
- Infección Respiratoria

## 📱 Integración con Apps

### Apps Web:
- CORS habilitado para cualquier origen
- Endpoints RESTful estándar
- Respuestas JSON estructuradas

### Apps Móviles:
- API compatible con React Native, Flutter, etc.
- Endpoints optimizados para consumo móvil
- Datos en tiempo real disponibles

## 🔐 Seguridad

- Validación de datos con Pydantic
- Manejo de errores HTTP estándar
- Preparado para autenticación JWT (comentado)
- Configuración de CORS personalizable

## 📈 Monitoreo y Logs

- Logs automáticos de la aplicación
- Scheduler para generación de datos
- Manejo de errores en base de datos
- Métricas de rendimiento disponibles

## 🚀 Próximos Pasos

1. **Conectar sensores reales** vía MQTT
2. **Implementar autenticación** JWT
3. **Añadir WebSockets** para tiempo real
4. **Integrar IA real** para predicciones
5. **Añadir notificaciones** push
6. **Implementar caching** con Redis

## 📞 Soporte

La API está completamente documentada y lista para uso. Para dudas específicas:
- Revisar documentación en `/docs`
- Ejecutar `test_api.py` para verificar funcionamiento
- Revisar logs en caso de errores
