from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GeneroEnum(str, Enum):
    M = "M"
    F = "F"

class PacienteBase(BaseModel):
    nombre: str
    edad: int
    genero: GeneroEnum
    activo: bool = True

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombre: Optional[str] = None
    edad: Optional[int] = None
    genero: Optional[GeneroEnum] = None
    activo: Optional[bool] = None

class PacienteResponse(PacienteBase):
    id: int
    
    class Config:
        from_attributes = True
