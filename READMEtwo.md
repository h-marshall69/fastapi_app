# Sistema de Monitoreo de Pacientes - API

## Descripción
API simulada para monitoreo de signos vitales en tiempo real usando FastAPI, diseñada para integrarse con sensores ESP32 y módulos MAX30102, DHT11, y DS18B20.

## Características
- ✅ API RESTful con FastAPI
- ✅ Base de datos MySQL
- ✅ Generación de datos simulados realistas
- ✅ Sistema de alertas automático
- ✅ Endpoints para predicciones (preparado para IA)
- ✅ Cliente MQTT para sensores ESP32
- ✅ Docker Compose para desarrollo
- ✅ Estructura modular y escalable

## Instalación

### Usando Docker (Recomendado)
```bash
# Clonar el repositorio
git clone <tu-repo>
cd api_medica

# Levantar servicios
docker-compose up -d

# Inicializar base de datos
python scripts/init_db.py
```

### Instalación Manual
```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar migraciones
python scripts/init_db.py

# Iniciar servidor
uvicorn app.main:app --reload
```

## Endpoints Principales

### Pacientes
- `POST /api/v1/pacientes/` - Crear paciente
- `GET /api/v1/pacientes/` - Listar pacientes
- `GET /api/v1/pacientes/{id}` - Obtener paciente
- `PUT /api/v1/pacientes/{id}` - Actualizar paciente
- `DELETE /api/v1/pacientes/{id}` - Eliminar paciente

### Mediciones
- `POST /api/v1/mediciones/` - Crear medición
- `GET /api/v1/mediciones/paciente/{id}` - Historial de mediciones
- `GET /api/v1/mediciones/paciente/{id}/ultima` - Última medición
- `POST /api/v1/mediciones/paciente/{id}/simular` - Simular medición

### Alertas
- `GET /api/v1/alertas/paciente/{id}` - Alertas por paciente
- `GET /api/v1/alertas/activas` - Alertas activas del sistema

### Predicciones
- `GET /api/v1/predicciones/paciente/{id}` - Predicciones por paciente
- `POST /api/v1/predicciones/paciente/{id}/simular` - Simular predicción

## Datos Simulados
Los datos generados respetan rangos realistas:
- **SpO2**: 95-100% (normal), 88-94% (anormal)
- **BPM**: 60-100 (normal), 45-59 o 101-125 (anormal)
- **Temperatura**: 36-38°C (normal), <36°C o >38°C (anormal)

## Sistema de Alertas
- 🟢 **Verde**: Signos vitales normales
- 🟡 **Amarilla**: Valores irregulares
- 🔴 **Roja**: Valores críticos

## Integración MQTT
El sistema está preparado para recibir datos de sensores ESP32 via MQTT:
```
Tópico: pacientes/monitoreo/{paciente_id}/mediciones
Payload: {"spo2": 98.5, "bpm": 72, "temperatura": 36.8}
```

## Scripts Útiles
```bash
# Inicializar base de datos con datos de prueba
python scripts/init_db.py

# Generar datos continuos (simular sensores)
python scripts/generate_test_data.py
```

## Estructura del Proyecto
```
api_medica/
├── app/
│   ├── main.py              # Punto de entrada
│   ├── database.py          # Configuración DB
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Esquemas Pydantic
│   ├── api/v1/              # Endpoints API
│   ├── services/            # Lógica de negocio
│   ├── core/                # Configuración
│   ├── mqtt/                # Cliente MQTT
│   └── utils/               # Utilidades
├── scripts/                 # Scripts de mantenimiento
├── tests/                   # Tests unitarios
└── docker-compose.yml       # Configuración Docker
```

## Próximos Pasos
1. **Conexión con sensores reales**: Configurar ESP32 con MQTT
2. **Integración de IA**: Implementar modelos de predicción
3. **Frontend**: Desarrollo de app web/móvil
4. **Autenticación**: Sistema de usuarios y roles
5. **Notificaciones**: Push notifications para alertas críticas

## Tecnologías Utilizadas
- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para base de datos
- **MySQL**: Base de datos relacional
- **Paho MQTT**: Cliente MQTT
- **Docker**: Contenedorización
- **Pydantic**: Validación de datos
