import paho.mqtt.publish as publish
import random
import time

paciente_id = 1  # ID del paciente de prueba

def generar_datos():
    """Genera datos aleatorios simulando los sensores"""
    return {
        "spo2": random.uniform(85.0, 99.9),  # SPO2 entre 85% y 99.9%
        "bpm": random.randint(50, 120),       # Ritmo cardíaco
        "temp": random.uniform(35.0, 39.5)    # Temperatura corporal
    }

def enviar_datos():
    while True:
        datos = generar_datos()
        payload = f"{paciente_id},{datos['spo2']:.1f},{datos['bpm']},{datos['temp']:.1f}"
        
        print(f"Enviando: {payload}")
        publish.single("pacientes/mediciones", payload, hostname="localhost")
        
        time.sleep(5)  # Envía datos cada 5 segundos

if __name__ == "__main__":
    enviar_datos()
