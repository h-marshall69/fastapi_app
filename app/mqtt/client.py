import paho.mqtt.client as mqtt
from app.core.config import settings
from app.database import SessionLocal
from app.services.mediciones import MedicionService
from app.schemas.medicion import MedicionCreate
import json
import logging

logger = logging.getLogger(__name__)

class MQTTClient:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Conectado al broker MQTT")
            # Suscribirse a todos los tópicos de mediciones
            client.subscribe(f"{settings.mqtt_topic_base}/+/mediciones")
        else:
            logger.error(f"Error conectando al broker MQTT: {rc}")
    
    def on_message(self, client, userdata, msg):
        try:
            # Parsear el tópico para obtener el ID del paciente
            topic_parts = msg.topic.split('/')
            if len(topic_parts) >= 3 and topic_parts[2] == 'mediciones':
                paciente_id = int(topic_parts[1])
                
                # Parsear los datos del mensaje
                data = json.loads(msg.payload.decode())
                
                # Crear la medición en la base de datos
                medicion_data = MedicionCreate(
                    id_paciente=paciente_id,
                    spo2=data['spo2'],
                    bpm=data['bpm'],
                    temperatura=data['temperatura']
                )
                
                db = SessionLocal()
                try:
                    service = MedicionService(db)
                    service.create(medicion_data)
                    logger.info(f"Medición guardada para paciente {paciente_id}")
                finally:
                    db.close()
                    
        except Exception as e:
            logger.error(f"Error procesando mensaje MQTT: {e}")
    
    def on_disconnect(self, client, userdata, rc):
        logger.info("Desconectado del broker MQTT")
    
    def start(self):
        self.client.connect(settings.mqtt_broker_host, settings.mqtt_broker_port, 60)
        self.client.loop_start()
    
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
    
    def publish_alert(self, paciente_id: int, alert_data: dict):
        """Publica una alerta via MQTT"""
        topic = f"{settings.mqtt_topic_base}/{paciente_id}/alertas"
        self.client.publish(topic, json.dumps(alert_data))
