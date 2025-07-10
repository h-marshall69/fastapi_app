from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import pacientes, mediciones, alertas, predicciones
from app.database import engine, Base
from app.mqtt.client import MQTTClient
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear instancia de FastAPI
app = FastAPI(
    title="Sistema de Monitoreo de Pacientes",
    description="API para monitoreo de signos vitales en tiempo real",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cliente MQTT global
mqtt_client = None

# Incluir routers
app.include_router(pacientes.router, prefix="/api/v1/pacientes", tags=["pacientes"])
app.include_router(mediciones.router, prefix="/api/v1/mediciones", tags=["mediciones"])
app.include_router(alertas.router, prefix="/api/v1/alertas", tags=["alertas"])
app.include_router(predicciones.router, prefix="/api/v1/predicciones", tags=["predicciones"])

@app.on_event("startup")
async def startup_event():
    """Inicializar servicios al arranque"""
    global mqtt_client
    try:
        mqtt_client = MQTTClient()
        mqtt_client.start()
        logger.info("Servicios iniciados correctamente")
    except Exception as e:
        logger.error(f"Error iniciando servicios: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Limpiar recursos al cierre"""
    global mqtt_client
    if mqtt_client:
        mqtt_client.stop()
        logger.info("Servicios detenidos correctamente")

@app.get("/")
async def root():
    return {
        "message": "Sistema de Monitoreo de Pacientes API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00"}
