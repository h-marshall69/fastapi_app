from sqlalchemy.orm import Session
from app.models.medicion import Medicion
from app.schemas.medicion import MedicionCreate
from typing import List, Optional
from datetime import datetime, timedelta
import random
from decimal import Decimal

class MedicionService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, medicion: MedicionCreate) -> Medicion:
        db_medicion = Medicion(**medicion.dict())
        self.db.add(db_medicion)
        self.db.commit()
        self.db.refresh(db_medicion)
        return db_medicion
    
    def get_by_paciente(self, paciente_id: int, skip: int = 0, limit: int = 100) -> List[Medicion]:
        return (self.db.query(Medicion)
                .filter(Medicion.id_paciente == paciente_id)
                .order_by(Medicion.timestamp.desc())
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_latest_by_paciente(self, paciente_id: int) -> Optional[Medicion]:
        return (self.db.query(Medicion)
                .filter(Medicion.id_paciente == paciente_id)
                .order_by(Medicion.timestamp.desc())
                .first())
    
    def get_by_date_range(self, paciente_id: int, start_date: datetime, end_date: datetime) -> List[Medicion]:
        return (self.db.query(Medicion)
                .filter(Medicion.id_paciente == paciente_id)
                .filter(Medicion.timestamp >= start_date)
                .filter(Medicion.timestamp <= end_date)
                .order_by(Medicion.timestamp.desc())
                .all())
    
    def generate_fake_medicion(self, paciente_id: int) -> Medicion:
        """Genera una medición falsa con datos realistas"""
        fake_data = MedicionCreate(
            id_paciente=paciente_id,
            spo2=Decimal(str(round(random.uniform(95.0, 100.0), 2))),
            bpm=random.randint(60, 100),
            temperatura=Decimal(str(round(random.uniform(36.0, 38.0), 2)))
        )
        return self.create(fake_data)
