import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_medicion():
    # Primero crear un paciente
    paciente_response = client.post("/api/v1/pacientes/", json={
        "nombre": "Test Paciente Medicion",
        "edad": 40,
        "genero": "M",
        "activo": True
    })
    paciente_id = paciente_response.json()["id"]
    
    # Crear medición
    response = client.post("/api/v1/mediciones/", json={
        "id_paciente": paciente_id,
        "spo2": 98.5,
        "bpm": 72,
        "temperatura": 36.8
    })
    assert response.status_code == 200
    data = response.json()
    assert data["spo2"] == 98.5
    assert data["bpm"] == 72

def test_simular_medicion():
    # Crear un paciente
    paciente_response = client.post("/api/v1/pacientes/", json={
        "nombre": "Test Paciente Simulacion",
        "edad": 35,
        "genero": "F",
        "activo": True
    })
    paciente_id = paciente_response.json()["id"]
    
    # Simular medición
    response = client.post(f"/api/v1/mediciones/paciente/{paciente_id}/simular")
    assert response.status_code == 200
    data = response.json()
    assert "spo2" in data
    assert "bpm" in data
    assert "temperatura" in data
