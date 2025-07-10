from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    genero = Column(Enum('M', 'F'), nullable=False)
    activo = Column(Boolean, default=True)
