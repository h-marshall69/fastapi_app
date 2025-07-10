from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import pacientes, mediciones, alertas, predicciones
from app.database import engine, Base
from app.mqtt.client import MQTTClient
from datetime import datetime
import logging
import psutil
import os
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app import models
from fastapi import Depends

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

# Configura CORS
origins = [
    "http://localhost:5000",  # Flask frontend
    "http://localhost:3000",  # React frontend
    "http://ip-de-tu-frontend"  # IP de tu frontend en producción
]

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    #allow_origins=["*"],  # En producción, especificar dominios específicos
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


def get_db_stats(db: Session = Depends(SessionLocal)):
    """Función auxiliar para obtener estadísticas de la base de datos"""
    return {
        "pacientes": db.query(models.Paciente).count(),
        "mediciones": db.query(models.Medicion).count(),
        "alertas": db.query(models.Alerta).count(),
        "predicciones": db.query(models.Prediccion).count()
    }

@app.get("/")
#async def root(db: Session = Depends(SessionLocal)):
async def root():
    """Endpoint raíz que muestra información relevante del sistema"""
    
    # Obtener información del sistema
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024  # en MB
    cpu_usage = psutil.cpu_percent()
    uptime = datetime.now() - start_time
    
    # Obtener estadísticas de la base de datos (ejemplo)
    db_stats = {
        "pacientes": 0,
        "mediciones": 0,
        "alertas": 0,
        "predicciones": 0
    }
    
    try:
        db_stats = get_db_stats(db)
    except Exception as e:
        print(f"Error obteniendo estadísticas de DB: {e}")
        db_stats = {
            "pacientes": "Error",
            "mediciones": "Error",
            "alertas": "Error",
            "predicciones": "Error"
        }    
    # Generar HTML con la información
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sistema de Monitoreo de Pacientes</title>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #3498db; }}
            .card {{ background: #f9f9f9; border-left: 4px solid #3498db; padding: 15px; margin: 15px 0; }}
            .stats {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }}
            .stat {{ background: #e8f4fc; padding: 10px; border-radius: 5px; }}
            .endpoints {{ margin-top: 20px; }}
            .endpoint {{ margin: 10px 0; padding: 10px; background: #f0f0f0; border-radius: 5px; }}
            .critical {{ color: #e74c3c; }}
            .warning {{ color: #f39c12; }}
            .ok {{ color: #27ae60; }}
        </style>
    </head>
    <body>
        <h1>🏥 Sistema de Monitoreo de Pacientes</h1>
        
        <div class="card">
            <h2>📊 Estadísticas del Sistema</h2>
            <div class="stats">
                <div class="stat">
                    <h3>Uso de Recursos</h3>
                    <p>Memoria: <strong>{memory_usage:.2f} MB</strong></p>
                    <p>CPU: <strong>{cpu_usage}%</strong></p>
                    <p>Tiempo activo: <strong>{str(uptime).split('.')[0]}</strong></p>
                </div>
                
                <div class="stat">
                    <h3>📦 Datos Almacenados</h3>
                    <p>Pacientes: <strong>{db_stats['pacientes']}</strong></p>
                    <p>Mediciones: <strong>{db_stats['mediciones']}</strong></p>
                    <p>Alertas: <strong>{db_stats['alertas']}</strong></p>
                    <p>Predicciones: <strong>{db_stats['predicciones']}</strong></p>
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🚀 Endpoints Disponibles</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <strong>GET /api/v1/pacientes/</strong> - Listar todos los pacientes
                </div>
                <div class="endpoint">
                    <strong>POST /api/v1/pacientes/</strong> - Crear nuevo paciente
                </div>
                <div class="endpoint">
                    <strong>GET /api/v1/mediciones/paciente/{id}</strong> - Obtener mediciones
                </div>
                <div class="endpoint">
                    <strong>POST /api/v1/mediciones/</strong> - Registrar medición
                </div>
                <div class="endpoint">
                    <strong>GET /api/v1/alertas/activas</strong> - Alertas recientes
                </div>
                <div class="endpoint">
                    <strong>GET /api/v1/predicciones/paciente/{id}</strong> - Predicciones
                </div>
            </div>
        </div>
        
        <div class="card">
            <h2>🔗 Enlaces Rápidos</h2>
            <ul>
                <li><a href="/docs" target="_blank">📚 Documentación interactiva (Swagger)</a></li>
                <li><a href="/redoc" target="_blank">📖 Documentación alternativa (ReDoc)</a></li>
                <li><a href="/health" target="_blank">🩺 Estado del sistema</a></li>
            </ul>
        </div>
        
        <footer>
            <p>🔄 Última actualización: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </footer>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00"}

# Variable para registrar el tiempo de inicio
start_time = datetime.now()
