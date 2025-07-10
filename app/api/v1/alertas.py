from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.alertas import AlertaService
from app.schemas.alerta import AlertaResponse
from typing import List

router = APIRouter()

@router.get("/paciente/{paciente_id}", response_model=List[AlertaResponse])
def get_alertas_paciente(
    paciente_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = AlertaService(db)
    return service.get_by_paciente(paciente_id, skip=skip, limit=limit)

@router.get("/activas", response_model=List[AlertaResponse])
def get_alertas_activas(db: Session = Depends(get_db)):
    service = AlertaService(db)
    return service.get_active_alerts()
