from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

# Esquemas para Pacientes
class PacienteBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    edad: int = Field(..., ge=0, le=120)
    genero: str = Field(..., pattern="^[MF]$")

class PacienteCreate(PacienteBase):
    activo: bool = True

class PacienteResponse(PacienteBase):
    id: int
    activo: bool
    
    class Config:
        from_attributes = True

# Esquemas para Mediciones
class MedicionBase(BaseModel):
    id_paciente: int
    spo2: Decimal = Field(..., ge=0, le=100)
    bpm: int = Field(..., ge=0, le=300)
    temperatura: Decimal = Field(..., ge=30, le=45)

class MedicionCreate(MedicionBase):
    pass

class MedicionResponse(MedicionBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Alertas
class AlertaResponse(BaseModel):
    id: int
    id_paciente: int
    tipo: str
    mensaje: str
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Predicciones
class PrediccionResponse(BaseModel):
    id: int
    id_paciente: int
    enfermedad: str
    probabilidad: Decimal
    timestamp: datetime
    
    class Config:
        from_attributes = True
