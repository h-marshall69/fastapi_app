from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class MedicionBase(BaseModel):
    spo2: Decimal
    bpm: int
    temperatura: Decimal

class MedicionCreate(MedicionBase):
    id_paciente: int

class MedicionResponse(MedicionBase):
    id: int
    id_paciente: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
