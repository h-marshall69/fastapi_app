"""
Módulo para manejar comunicación MQTT con ESP32
Este módulo será usado cuando se conecten los sensores reales
"""

import paho.mqtt.client as mqtt
import json
from typing import Callable

class MQTTHandler:
    """Manejador MQTT para recibir datos del ESP32"""
    
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.client = mqtt.Client()
        self.callback_function = None
        
        # Configurar callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback cuando se conecta al broker MQTT"""
        if rc == 0:
            print("Conectado al broker MQTT")
            # Suscribirse a tópicos de sensores
            client.subscribe("esp32/sensors/+/data")
            client.subscribe("esp32/health")
        else:
            print(f"Error conectando al broker MQTT: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Callback cuando se recibe un mensaje MQTT"""
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            
            if "sensors" in topic and self.callback_function:
                # Procesar datos de sensores
                self.callback_function(payload)
            
        except Exception as e:
            print(f"Error procesando mensaje MQTT: {e}")
    
    def set_data_callback(self, callback: Callable):
        """Establece la función callback para procesar datos"""
        self.callback_function = callback
    
    def start(self):
        """Inicia el cliente MQTT"""
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
        except Exception as e:
            print(f"Error iniciando cliente MQTT: {e}")
    
    def stop(self):
        """Detiene el cliente MQTT"""
        self.client.loop_stop()
        self.client.disconnect()

# Ejemplo de uso del MQTT Handler (comentado para desarrollo)
"""
def process_sensor_data(data):
    # Procesar datos recibidos del ESP32
    # Ejemplo de estructura esperada:
    # {
    #     "patient_id": 1,
    #     "bpm": 75,
    #     "spo2": 98.5,
    #     "body_temp": 36.8,
    #     "ambient_temp": 22.5,
    #     "timestamp": "2024-01-15T10:30:00"
    # }
    pass

# Inicializar MQTT cuando se tengan sensores reales
# mqtt_handler = MQTTHandler()
# mqtt_handler.set_data_callback(process_sensor_data)
# mqtt_handler.start()
"""
