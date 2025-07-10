from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

class PrediccionBase(BaseModel):
    enfermedad: str
    probabilidad: Decimal

class PrediccionCreate(PrediccionBase):
    id_paciente: int

class PrediccionResponse(PrediccionBase):
    id: int
    id_paciente: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
