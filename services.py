import random
from datetime import datetime, timedelta
from typing import Dict, Optional

class DataSimulationService:
    """Servicio para generar datos simulados realistas"""
    
    def __init__(self):
        self.prediction_counter = 0
    
    def generate_measurement(self, paciente_id: int, edad: int) -> Dict:
        """Genera una medición simulada basada en rangos realistas"""
        
        # Ajustar rangos según edad
        if edad < 30:
            bpm_base = (70, 90)
            spo2_base = (97, 100)
            temp_base = (36.2, 37.2)
        elif edad < 60:
            bpm_base = (65, 85)
            spo2_base = (96, 99)
            temp_base = (36.1, 37.1)
        else:
            bpm_base = (60, 80)
            spo2_base = (95, 98)
            temp_base = (36.0, 37.0)
        
        # Añadir variabilidad ocasional
        variabilidad = random.choice([0, 0, 0, 0, 1])  # 20% de probabilidad de variación
        
        if variabilidad:
            bpm = random.randint(bpm_base[0] - 15, bpm_base[1] + 20)
            spo2 = round(random.uniform(max(88, spo2_base[0] - 8), spo2_base[1]), 2)
            temperatura = round(random.uniform(temp_base[0] - 1, temp_base[1] + 2), 2)
        else:
            bpm = random.randint(bpm_base[0], bpm_base[1])
            spo2 = round(random.uniform(spo2_base[0], spo2_base[1]), 2)
            temperatura = round(random.uniform(temp_base[0], temp_base[1]), 2)
        
        return {
            "id_paciente": paciente_id,
            "bpm": bpm,
            "spo2": spo2,
            "temperatura": temperatura,
            "timestamp": datetime.now()
        }
    
    def should_generate_prediction(self) -> bool:
        """Determina si debe generar una predicción (cada ~10 mediciones)"""
        self.prediction_counter += 1
        if self.prediction_counter >= 10:
            self.prediction_counter = 0
            return True
        return False

class AlertService:
    """Servicio para evaluar y generar alertas"""
    
    def check_alert(self, medicion: Dict, edad: int) -> Optional[Dict]:
        """Evalúa si una medición requiere alerta"""
        
        bpm = medicion["bpm"]
        spo2 = float(medicion["spo2"])
        temperatura = float(medicion["temperatura"])
        
        # Alertas críticas (rojas)
        if bpm > 120 or bpm < 50:
            return {"tipo": "roja", "mensaje": f"Frecuencia cardíaca crítica: {bpm} BPM"}
        
        if spo2 < 90:
            return {"tipo": "roja", "mensaje": f"Saturación de oxígeno crítica: {spo2}%"}
        
        if temperatura > 39 or temperatura < 35:
            return {"tipo": "roja", "mensaje": f"Temperatura crítica: {temperatura}°C"}
        
        # Alertas de precaución (amarillas)
        if bpm > 100 or bpm < 60:
            return {"tipo": "amarilla", "mensaje": f"Frecuencia cardíaca elevada: {bpm} BPM"}
        
        if spo2 < 95:
            return {"tipo": "amarilla", "mensaje": f"Saturación de oxígeno baja: {spo2}%"}
        
        if temperatura > 37.5 or temperatura < 36:
            return {"tipo": "amarilla", "mensaje": f"Temperatura anormal: {temperatura}°C"}
        
        # Sin alertas
        return None

class PredictionService:
    """Servicio para generar predicciones simuladas de IA"""
    
    def __init__(self):
        self.enfermedades = [
            "Hipertensión", "Diabetes Tipo 2", "Arritmia Cardíaca",
            "Anemia", "Hipotiroidismo", "Infección Respiratoria",
            "Taquicardia", "Bradicardia", "Hipoxemia", "Fiebre"
        ]
    
    def generate_prediction(self, paciente_id: int) -> Dict:
        """Genera una predicción simulada"""
        
        enfermedad = random.choice(self.enfermedades)
        
        # Generar probabilidad realista
        if enfermedad in ["Hipertensión", "Diabetes Tipo 2"]:
            probabilidad = round(random.uniform(0.15, 0.45), 4)
        elif enfermedad in ["Arritmia Cardíaca", "Anemia"]:
            probabilidad = round(random.uniform(0.10, 0.35), 4)
        else:
            probabilidad = round(random.uniform(0.05, 0.25), 4)
        
        return {
            "id_paciente": paciente_id,
            "enfermedad": enfermedad,
            "probabilidad": probabilidad,
            "timestamp": datetime.now()
        }
