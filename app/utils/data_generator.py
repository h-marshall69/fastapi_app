import random
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.pacientes import PacienteService
from app.services.mediciones import MedicionService
from app.services.alertas import AlertaService
from app.services.predicciones import PrediccionService
from app.schemas.paciente import PacienteCreate
from app.schemas.medicion import MedicionCreate
from app.schemas.alerta import AlertaCreate, TipoAlertaEnum
from app.schemas.prediccion import PrediccionCreate

class DataGenerator:
    def __init__(self, db: Session):
        self.db = db
    
    def generate_sample_patients(self, count: int = 5):
        """Genera pacientes de muestra"""
        nombres = ["Juan Pérez", "María García", "Carlos López", "Ana Rodríguez", "Pedro Martínez"]
        service = PacienteService(self.db)
        
        for i in range(count):
            paciente = PacienteCreate(
                nombre=nombres[i % len(nombres)],
                edad=random.randint(18, 80),
                genero=random.choice(['M', 'F']),
                activo=True
            )
            service.create(paciente)
    
    def generate_historical_data(self, paciente_id: int, days: int = 7):
        """Genera datos históricos para un paciente"""
        service = MedicionService(self.db)
        alerta_service = AlertaService(self.db)
        
        # Generar mediciones cada hora durante los días especificados
        start_date = datetime.now() - timedelta(days=days)
        
        for hour in range(days * 24):
            timestamp = start_date + timedelta(hours=hour)
            
            # Generar datos con ligera variabilidad
            spo2 = Decimal(str(round(random.uniform(95.0, 100.0), 2)))
            bpm = random.randint(60, 100)
            temperatura = Decimal(str(round(random.uniform(36.0, 38.0), 2)))
            
            # Ocasionalmente generar valores anormales
            if random.random() < 0.1:  # 10% de probabilidad
                if random.choice([True, False]):
                    spo2 = Decimal(str(round(random.uniform(88.0, 94.0), 2)))
                else:
                    bpm = random.randint(45, 55) if random.choice([True, False]) else random.randint(105, 125)
            
            medicion = MedicionCreate(
                id_paciente=paciente_id,
                spo2=spo2,
                bpm=bpm,
                temperatura=temperatura
            )
            
            nueva_medicion = service.create(medicion)
            
            # Evaluar y crear alerta
            from app.schemas.medicion import MedicionResponse
            alerta_data = alerta_service.evaluate_medicion(MedicionResponse.from_orm(nueva_medicion))
            alerta_service.create(alerta_data)
    
    def generate_predictions(self, paciente_id: int, count: int = 5):
        """Genera predicciones de muestra para un paciente"""
        service = PrediccionService(self.db)
        
        for _ in range(count):
            service.generate_fake_prediction(paciente_id)
