from sqlalchemy.orm import Session
from app.models.alerta import Alerta
from app.schemas.alerta import AlertaCreate, TipoAlertaEnum
from app.schemas.medicion import MedicionResponse
from typing import List
from decimal import Decimal

class AlertaService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, alerta: AlertaCreate) -> Alerta:
        db_alerta = Alerta(**alerta.dict())
        self.db.add(db_alerta)
        self.db.commit()
        self.db.refresh(db_alerta)
        return db_alerta
    
    def get_by_paciente(self, paciente_id: int, skip: int = 0, limit: int = 100) -> List[Alerta]:
        return (self.db.query(Alerta)
                .filter(Alerta.id_paciente == paciente_id)
                .order_by(Alerta.timestamp.desc())
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_active_alerts(self) -> List[Alerta]:
        """Obtiene las alertas más recientes de cada paciente"""
        return (self.db.query(Alerta)
                .filter(Alerta.tipo.in_(['amarilla', 'roja']))
                .order_by(Alerta.timestamp.desc())
                .limit(50)
                .all())
    
    def evaluate_medicion(self, medicion: MedicionResponse) -> AlertaCreate:
        """Evalúa una medición y genera una alerta según los valores"""
        alertas = []
        
        # Evaluar SpO2
        if medicion.spo2 < 90:
            alertas.append(("SpO2 críticamente bajo", "roja"))
        elif medicion.spo2 < 95:
            alertas.append(("SpO2 bajo", "amarilla"))
        
        # Evaluar BPM
        if medicion.bpm < 50 or medicion.bpm > 120:
            alertas.append(("Ritmo cardíaco anormal", "roja"))
        elif medicion.bpm < 60 or medicion.bpm > 100:
            alertas.append(("Ritmo cardíaco irregular", "amarilla"))
        
        # Evaluar Temperatura
        if medicion.temperatura > 39 or medicion.temperatura < 35:
            alertas.append(("Temperatura crítica", "roja"))
        elif medicion.temperatura > 38 or medicion.temperatura < 36:
            alertas.append(("Temperatura anormal", "amarilla"))
        
        # Determinar la alerta más crítica
        if alertas:
            alertas_rojas = [a for a in alertas if a[1] == "roja"]
            if alertas_rojas:
                mensaje = "; ".join([a[0] for a in alertas_rojas])
                tipo = TipoAlertaEnum.roja
            else:
                mensaje = "; ".join([a[0] for a in alertas])
                tipo = TipoAlertaEnum.amarilla
        else:
            mensaje = "Signos vitales normales"
            tipo = TipoAlertaEnum.verde
        
        return AlertaCreate(
            id_paciente=medicion.id_paciente,
            tipo=tipo,
            mensaje=mensaje
        )
