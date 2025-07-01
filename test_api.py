"""
Script de prueba para verificar que la API funciona correctamente
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_api():
    """Prueba todos los endpoints principales de la API"""
    
    print("🧪 Iniciando pruebas de la API...")
    
    # 1. Verificar que la API está funcionando
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✅ API funcionando: {response.json()['mensaje']}")
    except Exception as e:
        print(f"❌ Error conectando a la API: {e}")
        return
    
    # 2. Generar datos de prueba
    print("\n📊 Generando datos de prueba...")
    try:
        response = requests.post(f"{BASE_URL}/utilidad/generar-datos-prueba")
        data = response.json()
        print(f"✅ {data['mensaje']}")
        print(f"   Pacientes creados: {data['pacientes_creados']}")
        print(f"   Mediciones generadas: {data['mediciones_generadas']}")
    except Exception as e:
        print(f"❌ Error generando datos: {e}")
    
    # 3. Obtener lista de pacientes
    print("\n👥 Obteniendo lista de pacientes...")
    try:
        response = requests.get(f"{BASE_URL}/pacientes/")
        pacientes = response.json()
        print(f"✅ Pacientes obtenidos: {len(pacientes)}")
        for p in pacientes[:3]:  # Mostrar solo los primeros 3
            print(f"   - {p['nombre']} ({p['edad']} años, {p['genero']})")
        
        # Usar el primer paciente para las siguientes pruebas
        if pacientes:
            paciente_id = pacientes[0]['id']
            print(f"🎯 Usando paciente ID {paciente_id} para pruebas")
        else:
            print("❌ No hay pacientes disponibles")
            return
            
    except Exception as e:
        print(f"❌ Error obteniendo pacientes: {e}")
        return
    
    # 4. Obtener mediciones del paciente
    print(f"\n📈 Obteniendo mediciones del paciente {paciente_id}...")
    try:
        response = requests.get(f"{BASE_URL}/mediciones/?paciente_id={paciente_id}&limit=5")
        mediciones = response.json()
        print(f"✅ Mediciones obtenidas: {len(mediciones)}")
        for m in mediciones[:2]:  # Mostrar solo las primeras 2
            print(f"   - BPM: {m['bpm']}, SpO2: {m['spo2']}%, Temp: {m['temperatura']}°C")
    except Exception as e:
        print(f"❌ Error obteniendo mediciones: {e}")
    
    # 5. Obtener datos en tiempo real
    print(f"\n⏱️ Obteniendo datos en tiempo real del paciente {paciente_id}...")
    try:
        response = requests.get(f"{BASE_URL}/mediciones/tiempo-real/{paciente_id}")
        data = response.json()
        print(f"✅ Datos en tiempo real obtenidos")
        print(f"   Paciente: {data['paciente']['nombre']}")
        print(f"   Mediciones recientes: {len(data['mediciones'])}")
        if data['ultima_alerta']:
            print(f"   Última alerta: {data['ultima_alerta']['tipo']} - {data['ultima_alerta']['mensaje']}")
    except Exception as e:
        print(f"❌ Error obteniendo datos en tiempo real: {e}")
    
    # 6. Obtener alertas
    print(f"\n🚨 Obteniendo alertas del paciente {paciente_id}...")
    try:
        response = requests.get(f"{BASE_URL}/alertas/?paciente_id={paciente_id}&limit=3")
        alertas = response.json()
        print(f"✅ Alertas obtenidas: {len(alertas)}")
        for a in alertas:
            print(f"   - {a['tipo'].upper()}: {a['mensaje']}")
    except Exception as e:
        print(f"❌ Error obteniendo alertas: {e}")
    
    # 7. Obtener predicciones
    print(f"\n🔮 Obteniendo predicciones del paciente {paciente_id}...")
    try:
        response = requests.get(f"{BASE_URL}/predicciones/?paciente_id={paciente_id}&limit=3")
        predicciones = response.json()
        print(f"✅ Predicciones obtenidas: {len(predicciones)}")
        for p in predicciones:
            print(f"   - {p['enfermedad']}: {float(p['probabilidad'])*100:.1f}% probabilidad")
    except Exception as e:
        print(f"❌ Error obteniendo predicciones: {e}")
    
    # 8. Obtener dashboard
    print(f"\n📊 Obteniendo dashboard del paciente {paciente_id}...")
    try:
        response = requests.get(f"{BASE_URL}/estadisticas/dashboard/{paciente_id}")
        dashboard = response.json()
        stats = dashboard['estadisticas']
        print(f"✅ Dashboard obtenido")
        print(f"   Total mediciones (24h): {stats['total_mediciones']}")
        print(f"   Promedio BPM: {stats['promedio_bpm']}")
        print(f"   Promedio SpO2: {stats['promedio_spo2']}%")
        print(f"   Promedio Temperatura: {stats['promedio_temperatura']}°C")
    except Exception as e:
        print(f"❌ Error obteniendo dashboard: {e}")
    
    # 9. Crear nueva medición (simulando sensor)
    print(f"\n📝 Creando nueva medición para paciente {paciente_id}...")
    try:
        nueva_medicion = {
            "id_paciente": paciente_id,
            "bpm": 78,
            "spo2": 97.5,
            "temperatura": 36.8
        }
        response = requests.post(f"{BASE_URL}/mediciones/", json=nueva_medicion)
        medicion_creada = response.json()
        print(f"✅ Medición creada con ID: {medicion_creada['id']}")
    except Exception as e:
        print(f"❌ Error creando medición: {e}")
    
    # 10. Generar predicción
    print(f"\n🔮 Generando nueva predicción para paciente {paciente_id}...")
    try:
        response = requests.post(f"{BASE_URL}/predicciones/generar/{paciente_id}")
        prediccion = response.json()
        print(f"✅ Predicción generada: {prediccion['enfermedad']} ({float(prediccion['probabilidad'])*100:.1f}%)")
    except Exception as e:
        print(f"❌ Error generando predicción: {e}")
    
    print("\n🎉 Pruebas completadas!")
    print(f"📚 Visita http://localhost:8000/docs para ver la documentación interactiva")

if __name__ == "__main__":
    test_api()
