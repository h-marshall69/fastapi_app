from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, DateTime, Enum, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    edad = Column(Integer, nullable=False)
    genero = Column(Enum('M', 'F'), nullable=False)
    activo = Column(Boolean, default=True)
    
    # Relaciones
    mediciones = relationship("Medicion", back_populates="paciente")
    alertas = relationship("Alerta", back_populates="paciente")
    predicciones = relationship("Prediccion", back_populates="paciente")

class Medicion(Base):
    __tablename__ = "mediciones"
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp())
    spo2 = Column(DECIMAL(5, 2), nullable=False)
    bpm = Column(Integer, nullable=False)
    temperatura = Column(DECIMAL(4, 2), nullable=False)
    
    # Relación
    paciente = relationship("Paciente", back_populates="mediciones")

class Alerta(Base):
    __tablename__ = "alertas"
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(Enum('verde', 'amarilla', 'roja'), nullable=False)
    mensaje = Column(String(255), nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp())
    
    # Relación
    paciente = relationship("Paciente", back_populates="alertas")

class Prediccion(Base):
    __tablename__ = "predicciones"
    
    id = Column(BIGINT, primary_key=True, autoincrement=True)
    id_paciente = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    enfermedad = Column(String(100), nullable=False)
    probabilidad = Column(DECIMAL(5, 4), nullable=False)
    timestamp = Column(DateTime, default=func.current_timestamp())
    
    # Relación
    paciente = relationship("Paciente", back_populates="predicciones")
