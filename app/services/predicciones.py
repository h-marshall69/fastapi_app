from sqlalchemy.orm import Session
from app.models.prediccion import Prediccion
from app.schemas.prediccion import PrediccionCreate
from typing import List
import random
from decimal import Decimal

class PrediccionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, prediccion: PrediccionCreate) -> Prediccion:
        db_prediccion = Prediccion(**prediccion.dict())
        self.db.add(db_prediccion)
        self.db.commit()
        self.db.refresh(db_prediccion)
        return db_prediccion
    
    def get_by_paciente(self, paciente_id: int, skip: int = 0, limit: int = 100) -> List[Prediccion]:
        return (self.db.query(Prediccion)
                .filter(Prediccion.id_paciente == paciente_id)
                .order_by(Prediccion.timestamp.desc())
                .offset(skip)
                .limit(limit)
                .all())
    
    def generate_fake_prediction(self, paciente_id: int) -> Prediccion:
        """Genera una predicción falsa para demostración"""
        enfermedades = [
            "Hipertensión",
            "Diabetes",
            "Arritmia",
            "Hipoxia",
            "Fiebre",
            "Bradicardia",
            "Taquicardia"
        ]
        
        fake_data = PrediccionCreate(
            id_paciente=paciente_id,
            enfermedad=random.choice(enfermedades),
            probabilidad=Decimal(str(round(random.uniform(0.1, 0.9), 4)))
        )
        return self.create(fake_data)
