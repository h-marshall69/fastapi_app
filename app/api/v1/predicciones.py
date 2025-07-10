from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.predicciones import PrediccionService
from app.schemas.prediccion import PrediccionResponse
from typing import List

router = APIRouter()

@router.get("/paciente/{paciente_id}", response_model=List[PrediccionResponse])
def get_predicciones_paciente(
    paciente_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    service = PrediccionService(db)
    return service.get_by_paciente(paciente_id, skip=skip, limit=limit)

@router.post("/paciente/{paciente_id}/simular", response_model=PrediccionResponse)
def simular_prediccion(paciente_id: int, db: Session = Depends(get_db)):
    """Genera una predicción falsa para demostración"""
    service = PrediccionService(db)
    return service.generate_fake_prediction(paciente_id)
