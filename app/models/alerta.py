from sqlalchemy import Column, Integer, BigInteger, String, Enum, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Alerta(Base):
    __tablename__ = "alertas"
    
    id = Column(BigInteger, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(Enum('verde', 'amarilla', 'roja'), nullable=False)
    mensaje = Column(String(255), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
