import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'app_pacientes',
    'password': 'password_seguro',
    'database': 'pacientes_monitoreo'
}

# Callback cuando se recibe un mensaje
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode().split(',')
        paciente_id = int(data[0])
        spo2 = float(data[1])
        bpm = int(data[2])
        temperatura = float(data[3])
        
        # Insertar datos en MySQL
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        query = """
        INSERT INTO mediciones (id_paciente, spo2, bpm, temperatura)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (paciente_id, spo2, bpm, temperatura))
        conn.commit()
        
        # Verificar alertas
        check_alerts(paciente_id, spo2, bpm, temperatura, cursor)
        
        cursor.close()
        conn.close()
        
        print(f"Datos insertados para paciente {paciente_id}")
        
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

def check_alerts(paciente_id, spo2, bpm, temperatura, cursor):
    # Lógica para determinar alertas
    alerta = None
    mensaje = ""
    
    if spo2 < 90:
        alerta = "roja"
        mensaje = f"SPO2 crítico: {spo2}%"
    elif bpm > 120 or bpm < 50:
        alerta = "amarilla"
        mensaje = f"Ritmo cardíaco anormal: {bpm} BPM"
    elif temperatura > 38.5:
        alerta = "amarilla"
        mensaje = f"Fiebre detectada: {temperatura}°C"
    
    if alerta:
        query = """
        INSERT INTO alertas (id_paciente, tipo, mensaje)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (paciente_id, alerta, mensaje))
        cursor.connection.commit()
        print(f"Alerta {alerta} generada: {mensaje}")

# Configurar cliente MQTT
client = mqtt.Client()
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.subscribe("pacientes/mediciones")

print("Cliente MQTT iniciado, esperando datos...")
client.loop_forever()
