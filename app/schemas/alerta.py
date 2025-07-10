from pydantic import BaseModel
from datetime import datetime
from enum import Enum

class TipoAlertaEnum(str, Enum):
    verde = "verde"
    amarilla = "amarilla"
    roja = "roja"

class AlertaBase(BaseModel):
    tipo: TipoAlertaEnum
    mensaje: str

class AlertaCreate(AlertaBase):
    id_paciente: int

class AlertaResponse(AlertaBase):
    id: int
    id_paciente: int
    timestamp: datetime
    
    class Config:
        from_attributes = True
