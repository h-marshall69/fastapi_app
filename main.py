from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from database import SessionLocal, engine, Base
from models import Paciente, Medicion, Alerta, Prediccion
from schemas import (
    PacienteCreate, PacienteResponse, 
    MedicionCreate, MedicionResponse,
    AlertaResponse, PrediccionResponse
)
from services import DataSimulationService, AlertService, PredictionService

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema de Monitoreo de Pacientes",
    description="API para monitoreo de signos vitales en tiempo real",
    version="1.0.0"
)

# Configurar CORS para apps web y móviles
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicializar servicios
data_service = DataSimulationService()
alert_service = AlertService()
prediction_service = PredictionService()

# Configurar scheduler para generar datos automáticamente
scheduler = BackgroundScheduler()

def generate_automatic_data():
    """Genera datos automáticamente cada 30 segundos para simulación"""
    db = SessionLocal()
    try:
        # Obtener pacientes activos
        pacientes = db.query(Paciente).filter(Paciente.activo == True).all()
        
        for paciente in pacientes:
            # Generar nueva medición
            medicion_data = data_service.generate_measurement(paciente.id, paciente.edad)
            nueva_medicion = Medicion(**medicion_data)
            db.add(nueva_medicion)
            
            # Verificar si necesita alerta
            alerta = alert_service.check_alert(medicion_data, paciente.edad)
            if alerta:
                nueva_alerta = Alerta(
                    id_paciente=paciente.id,
                    tipo=alerta['tipo'],
                    mensaje=alerta['mensaje']
                )
                db.add(nueva_alerta)
            
            # Generar predicción ocasionalmente (cada 5 minutos aprox)
            if data_service.should_generate_prediction():
                prediccion_data = prediction_service.generate_prediction(paciente.id)
                nueva_prediccion = Prediccion(**prediccion_data)
                db.add(nueva_prediccion)
        
        db.commit()
    except Exception as e:
        print(f"Error generando datos automáticos: {e}")
        db.rollback()
    finally:
        db.close()

# Programar generación automática de datos cada 30 segundos
scheduler.add_job(
    func=generate_automatic_data,
    trigger="interval",
    seconds=30,
    id='auto_data_generation'
)
scheduler.start()

# Cerrar scheduler al terminar la aplicación
atexit.register(lambda: scheduler.shutdown())

# ========== ENDPOINTS DE PACIENTES ==========

@app.post("/pacientes/", response_model=PacienteResponse)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo paciente"""
    db_paciente = Paciente(**paciente.dict())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    return db_paciente

@app.get("/pacientes/", response_model=List[PacienteResponse])
def obtener_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Obtener lista de pacientes"""
    pacientes = db.query(Paciente).offset(skip).limit(limit).all()
    return pacientes

@app.get("/pacientes/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener información de un paciente específico"""
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

# ========== ENDPOINTS DE MEDICIONES ==========

@app.get("/mediciones/", response_model=List[MedicionResponse])
def obtener_mediciones(
    paciente_id: Optional[int] = None,
    horas: Optional[int] = 24,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener mediciones con filtros opcionales"""
    query = db.query(Medicion)
    
    if paciente_id:
        query = query.filter(Medicion.id_paciente == paciente_id)
    
    if horas:
        fecha_limite = datetime.now() - timedelta(hours=horas)
        query = query.filter(Medicion.timestamp >= fecha_limite)
    
    mediciones = query.order_by(Medicion.timestamp.desc()).offset(skip).limit(limit).all()
    return mediciones

@app.post("/mediciones/", response_model=MedicionResponse)
def crear_medicion(medicion: MedicionCreate, db: Session = Depends(get_db)):
    """Crear una nueva medición (para cuando se conecten sensores reales)"""
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == medicion.id_paciente).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db_medicion = Medicion(**medicion.dict())
    db.add(db_medicion)
    db.commit()
    db.refresh(db_medicion)
    
    # Verificar si necesita generar alerta
    alerta = alert_service.check_alert(medicion.dict(), paciente.edad)
    if alerta:
        nueva_alerta = Alerta(
            id_paciente=medicion.id_paciente,
            tipo=alerta['tipo'],
            mensaje=alerta['mensaje']
        )
        db.add(nueva_alerta)
        db.commit()
    
    return db_medicion

@app.get("/mediciones/tiempo-real/{paciente_id}")
def obtener_mediciones_tiempo_real(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener las últimas mediciones en tiempo real de un paciente"""
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Obtener últimas 10 mediciones
    mediciones = db.query(Medicion).filter(
        Medicion.id_paciente == paciente_id
    ).order_by(Medicion.timestamp.desc()).limit(10).all()
    
    # Obtener última alerta si existe
    ultima_alerta = db.query(Alerta).filter(
        Alerta.id_paciente == paciente_id
    ).order_by(Alerta.timestamp.desc()).first()
    
    return {
        "paciente": paciente,
        "mediciones": mediciones,
        "ultima_alerta": ultima_alerta,
        "timestamp": datetime.now()
    }

# ========== ENDPOINTS DE ALERTAS ==========

@app.get("/alertas/", response_model=List[AlertaResponse])
def obtener_alertas(
    paciente_id: Optional[int] = None,
    tipo: Optional[str] = None,
    horas: Optional[int] = 24,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener alertas con filtros opcionales"""
    query = db.query(Alerta)
    
    if paciente_id:
        query = query.filter(Alerta.id_paciente == paciente_id)
    
    if tipo:
        query = query.filter(Alerta.tipo == tipo)
    
    if horas:
        fecha_limite = datetime.now() - timedelta(hours=horas)
        query = query.filter(Alerta.timestamp >= fecha_limite)
    
    alertas = query.order_by(Alerta.timestamp.desc()).offset(skip).limit(limit).all()
    return alertas

@app.get("/alertas/criticas")
def obtener_alertas_criticas(db: Session = Depends(get_db)):
    """Obtener alertas críticas (rojas) de las últimas 2 horas"""
    fecha_limite = datetime.now() - timedelta(hours=2)
    alertas = db.query(Alerta).filter(
        Alerta.tipo == 'roja',
        Alerta.timestamp >= fecha_limite
    ).order_by(Alerta.timestamp.desc()).all()
    
    return {
        "total": len(alertas),
        "alertas": alertas
    }

# ========== ENDPOINTS DE PREDICCIONES ==========

@app.get("/predicciones/", response_model=List[PrediccionResponse])
def obtener_predicciones(
    paciente_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Obtener predicciones de IA"""
    query = db.query(Prediccion)
    
    if paciente_id:
        query = query.filter(Prediccion.id_paciente == paciente_id)
    
    predicciones = query.order_by(Prediccion.timestamp.desc()).offset(skip).limit(limit).all()
    return predicciones

@app.post("/predicciones/generar/{paciente_id}")
def generar_prediccion(paciente_id: int, db: Session = Depends(get_db)):
    """Generar nueva predicción para un paciente específico"""
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Generar predicción
    prediccion_data = prediction_service.generate_prediction(paciente_id)
    nueva_prediccion = Prediccion(**prediccion_data)
    db.add(nueva_prediccion)
    db.commit()
    db.refresh(nueva_prediccion)
    
    return nueva_prediccion

# ========== ENDPOINTS DE ESTADÍSTICAS ==========

@app.get("/estadisticas/dashboard/{paciente_id}")
def obtener_dashboard(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener datos para dashboard del paciente"""
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Obtener mediciones de las últimas 24 horas
    fecha_limite = datetime.now() - timedelta(hours=24)
    mediciones = db.query(Medicion).filter(
        Medicion.id_paciente == paciente_id,
        Medicion.timestamp >= fecha_limite
    ).order_by(Medicion.timestamp.desc()).all()
    
    # Obtener alertas recientes
    alertas = db.query(Alerta).filter(
        Alerta.id_paciente == paciente_id,
        Alerta.timestamp >= fecha_limite
    ).order_by(Alerta.timestamp.desc()).limit(5).all()
    
    # Obtener última predicción
    ultima_prediccion = db.query(Prediccion).filter(
        Prediccion.id_paciente == paciente_id
    ).order_by(Prediccion.timestamp.desc()).first()
    
    # Calcular promedios
    if mediciones:
        promedio_bpm = sum(m.bpm for m in mediciones) / len(mediciones)
        promedio_spo2 = sum(float(m.spo2) for m in mediciones) / len(mediciones)
        promedio_temp = sum(float(m.temperatura) for m in mediciones) / len(mediciones)
    else:
        promedio_bpm = promedio_spo2 = promedio_temp = 0
    
    return {
        "paciente": paciente,
        "estadisticas": {
            "total_mediciones": len(mediciones),
            "promedio_bpm": round(promedio_bpm, 1),
            "promedio_spo2": round(promedio_spo2, 1),
            "promedio_temperatura": round(promedio_temp, 1)
        },
        "mediciones_recientes": mediciones[:10],
        "alertas_recientes": alertas,
        "ultima_prediccion": ultima_prediccion
    }

# ========== ENDPOINTS PARA INTEGRACIÓN MQTT (Preparado para ESP32) ==========

@app.post("/mqtt/medicion")
def recibir_medicion_mqtt(medicion: MedicionCreate, db: Session = Depends(get_db)):
    """Endpoint para recibir mediciones desde ESP32 vía MQTT"""
    # Este endpoint será usado cuando se implemente MQTT
    return crear_medicion(medicion, db)

# ========== ENDPOINTS DE UTILIDAD ==========

@app.post("/utilidad/generar-datos-prueba")
def generar_datos_prueba(db: Session = Depends(get_db)):
    """Generar datos de prueba para desarrollo"""
    try:
        # Crear pacientes de prueba si no existen
        pacientes_prueba = [
            {"nombre": "Juan Pérez", "edad": 45, "genero": "M"},
            {"nombre": "María García", "edad": 32, "genero": "F"},
            {"nombre": "Carlos López", "edad": 67, "genero": "M"},
            {"nombre": "Ana Martínez", "edad": 28, "genero": "F"}
        ]
        
        pacientes_creados = []
        for paciente_data in pacientes_prueba:
            # Verificar si ya existe
            existe = db.query(Paciente).filter(Paciente.nombre == paciente_data["nombre"]).first()
            if not existe:
                paciente = Paciente(**paciente_data)
                db.add(paciente)
                db.commit()
                db.refresh(paciente)
                pacientes_creados.append(paciente)
        
        # Generar mediciones para cada paciente
        total_mediciones = 0
        for paciente in db.query(Paciente).all():
            for _ in range(10):  # 10 mediciones por paciente
                medicion_data = data_service.generate_measurement(paciente.id, paciente.edad)
                medicion = Medicion(**medicion_data)
                db.add(medicion)
                total_mediciones += 1
        
        db.commit()
        
        return {
            "mensaje": "Datos de prueba generados exitosamente",
            "pacientes_creados": len(pacientes_creados),
            "mediciones_generadas": total_mediciones
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error generando datos: {str(e)}")

@app.get("/")
def read_root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "Sistema de Monitoreo de Pacientes API",
        "version": "1.0.0",
        "estado": "Funcionando",
        "documentacion": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
