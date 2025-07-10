#!/usr/bin/env python3
"""
Script para inicializar la base de datos con datos de prueba
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine, Base
from app.utils.data_generator import DataGenerator

def init_database():
    """Inicializa la base de datos con datos de prueba"""
    print("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        generator = DataGenerator(db)
        
        print("Generando pacientes de muestra...")
        generator.generate_sample_patients(5)
        
        print("Generando datos históricos...")
        for paciente_id in range(1, 6):
            generator.generate_historical_data(paciente_id, days=7)
            generator.generate_predictions(paciente_id, count=3)
        
        print("Base de datos inicializada exitosamente!")
        
    except Exception as e:
        print(f"Error inicializando base de datos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
