from sqlalchemy import Column, Integer, BigInteger, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Medicion(Base):
    __tablename__ = "mediciones"
    
    id = Column(BigInteger, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
    spo2 = Column(DECIMAL(5, 2), nullable=False)
    bpm = Column(Integer, nullable=False)
    temperatura = Column(DECIMAL(4, 2), nullable=False)
