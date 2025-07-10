from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.mediciones import MedicionService
from app.services.alertas import AlertaService
from app.schemas.medicion import MedicionCreate, MedicionResponse
from typing import List, Optional
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=MedicionResponse)
def create_medicion(medicion: MedicionCreate, db: Session = Depends(get_db)):
    service = MedicionService(db)
    nueva_medicion = service.create(medicion)
    
    # Evaluar y crear alerta si es necesario
    alerta_service = AlertaService(db)
    alerta_data = alerta_service.evaluate_medicion(MedicionResponse.from_orm(nueva_medicion))
    alerta_service.create(alerta_data)
    
    return nueva_medicion

@router.get("/paciente/{paciente_id}", response_model=List[MedicionResponse])
def get_mediciones_paciente(
    paciente_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = MedicionService(db)
    return service.get_by_paciente(paciente_id, skip=skip, limit=limit)

@router.get("/paciente/{paciente_id}/ultima", response_model=MedicionResponse)
def get_ultima_medicion_paciente(paciente_id: int, db: Session = Depends(get_db)):
    service = MedicionService(db)
    medicion = service.get_latest_by_paciente(paciente_id)
    if not medicion:
        raise HTTPException(status_code=404, detail="No hay mediciones para este paciente")
    return medicion

@router.get("/paciente/{paciente_id}/rango", response_model=List[MedicionResponse])
def get_mediciones_rango(
    paciente_id: int,
    start_date: datetime = Query(..., description="Fecha de inicio (YYYY-MM-DD HH:MM:SS)"),
    end_date: datetime = Query(..., description="Fecha de fin (YYYY-MM-DD HH:MM:SS)"),
    db: Session = Depends(get_db)
):
    service = MedicionService(db)
    return service.get_by_date_range(paciente_id, start_date, end_date)

@router.post("/paciente/{paciente_id}/simular", response_model=MedicionResponse)
def simular_medicion(paciente_id: int, db: Session = Depends(get_db)):
    """Genera una medición falsa para pruebas"""
    service = MedicionService(db)
    medicion = service.generate_fake_medicion(paciente_id)
    
    # Evaluar y crear alerta
    alerta_service = AlertaService(db)
    alerta_data = alerta_service.evaluate_medicion(MedicionResponse.from_orm(medicion))
    alerta_service.create(alerta_data)
    
    return medicion
