#!/usr/bin/env python3
"""
Script para generar datos de prueba continuos
"""

import sys
import os
import time
import random
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.services.mediciones import MedicionService
from app.services.alertas import AlertaService
from app.schemas.medicion import MedicionResponse

def generate_continuous_data():
    """Genera datos continuos para simular sensores en tiempo real"""
    db = SessionLocal()
    
    try:
        medicion_service = MedicionService(db)
        alerta_service = AlertaService(db)
        
        print("Generando datos continuos... (Ctrl+C para detener)")
        
        while True:
            # Generar datos para pacientes 1-5
            for paciente_id in range(1, 6):
                medicion = medicion_service.generate_fake_medicion(paciente_id)
                
                # Evaluar y crear alerta
                alerta_data = alerta_service.evaluate_medicion(MedicionResponse.from_orm(medicion))
                alerta_service.create(alerta_data)
                
                print(f"Paciente {paciente_id}: SpO2={medicion.spo2}%, BPM={medicion.bpm}, Temp={medicion.temperatura}°C")
            
            # Esperar antes de la siguiente iteración
            time.sleep(random.randint(30, 120))  # Entre 30 segundos y 2 minutos
            
    except KeyboardInterrupt:
        print("\nDeteniendo generación de datos...")
    finally:
        db.close()

if __name__ == "__main__":
    generate_continuous_data()
