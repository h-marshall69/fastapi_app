from sqlalchemy import Column, Integer, BigInteger, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Prediccion(Base):
    __tablename__ = "predicciones"
    
    id = Column(BigInteger, primary_key=True, index=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    enfermedad = Column(String(100), nullable=False)
    probabilidad = Column(DECIMAL(5, 4), nullable=False)
    timestamp = Column(TIMESTAMP, default=func.current_timestamp())
