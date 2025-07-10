from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.pacientes import PacienteService
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=PacienteResponse)
def create_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.create(paciente)

@router.get("/", response_model=List[PacienteResponse])
def get_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.get_all(skip=skip, limit=limit)

@router.get("/activos", response_model=List[PacienteResponse])
def get_pacientes_activos(db: Session = Depends(get_db)):
    service = PacienteService(db)
    return service.get_active()

@router.get("/{paciente_id}", response_model=PacienteResponse)
def get_paciente(paciente_id: int, db: Session = Depends(get_db)):
    service = PacienteService(db)
    paciente = service.get_by_id(paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
def update_paciente(paciente_id: int, paciente_update: PacienteUpdate, db: Session = Depends(get_db)):
    service = PacienteService(db)
    paciente = service.update(paciente_id, paciente_update)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return paciente

@router.delete("/{paciente_id}")
def delete_paciente(paciente_id: int, db: Session = Depends(get_db)):
    service = PacienteService(db)
    if not service.delete(paciente_id):
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    return {"message": "Paciente eliminado exitosamente"}
