import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_paciente():
    response = client.post("/api/v1/pacientes/", json={
        "nombre": "Test Paciente",
        "edad": 30,
        "genero": "M",
        "activo": True
    })
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Paciente"
    assert data["edad"] == 30

def test_get_pacientes():
    response = client.get("/api/v1/pacientes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_paciente_by_id():
    # Primero crear un paciente
    create_response = client.post("/api/v1/pacientes/", json={
        "nombre": "Test Paciente 2",
        "edad": 25,
        "genero": "F",
        "activo": True
    })
    paciente_id = create_response.json()["id"]
    
    # Luego obtenerlo
    response = client.get(f"/api/v1/pacientes/{paciente_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Test Paciente 2"
