from flask import Flask, render_template
import requests

app = Flask(__name__)

# Configuración - apunta a tu API
API_BASE_URL = "http://ip-de-tu-api:8001/api/v1"  # Cambia esto

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    try:
        # Obtener datos de la API
        pacientes = requests.get(f"{API_BASE_URL}/pacientes/").json()
        alertas = requests.get(f"{API_BASE_URL}/alertas/activas").json()
        
        return render_template('dashboard.html', 
                            pacientes=pacientes,
                            alertas=alertas)
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
