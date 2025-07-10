from sqlalchemy.orm import Session
from app.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate
from typing import List, Optional

class PacienteService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, paciente: PacienteCreate) -> Paciente:
        db_paciente = Paciente(**paciente.dict())
        self.db.add(db_paciente)
        self.db.commit()
        self.db.refresh(db_paciente)
        return db_paciente
    
    def get_by_id(self, paciente_id: int) -> Optional[Paciente]:
        return self.db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Paciente]:
        return self.db.query(Paciente).offset(skip).limit(limit).all()
    
    def get_active(self) -> List[Paciente]:
        return self.db.query(Paciente).filter(Paciente.activo == True).all()
    
    def update(self, paciente_id: int, paciente_update: PacienteUpdate) -> Optional[Paciente]:
        db_paciente = self.get_by_id(paciente_id)
        if not db_paciente:
            return None
        
        update_data = paciente_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_paciente, field, value)
        
        self.db.commit()
        self.db.refresh(db_paciente)
        return db_paciente
    
    def delete(self, paciente_id: int) -> bool:
        db_paciente = self.get_by_id(paciente_id)
        if not db_paciente:
            return False
        
        self.db.delete(db_paciente)
        self.db.commit()
        return True
