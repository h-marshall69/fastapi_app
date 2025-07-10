"""
Script mejorado con verificación de servicios Docker
"""

import subprocess
import sys
import time
import docker
import uvicorn
from app.main import app

def check_docker_services():
    """Verifica que los servicios Docker estén corriendo"""
    print("\n🐳 Verificando servicios Docker...")
    try:
        client = docker.from_env()
        services = {
            "mysql": False,
            "redis": False,
            "mosquitto": False
        }
        
        for container in client.containers.list():
            if "mysql" in container.name.lower():
                services["mysql"] = True
            elif "redis" in container.name.lower():
                services["redis"] = True
            elif "mosquitto" in container.name.lower():
                services["mosquitto"] = True
        
        all_running = all(services.values())
        
        if all_running:
            print("✅ Todos los servicios Docker están corriendo")
        else:
            print("⚠️ Servicios Docker faltantes:")
            for service, running in services.items():
                if not running:
                    print(f" - {service}")
            
            print("\n💡 Ejecuta: docker-compose up -d")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Error al verificar Docker: {e}")
        return False

def run_init_db():
    """Ejecuta el script de inicialización de la base de datos"""
    print("\n🔍 Verificando estado de la base de datos...")
    try:
        result = subprocess.run(
            [sys.executable, "scripts/init_db.py"],
            check=True,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print("✅ Base de datos inicializada correctamente")
            print(result.stdout)
        
        if result.stderr:
            print("⚠️ Advertencias durante la inicialización:")
            print(result.stderr)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        print("Salida del error:")
        print(e.stderr)
        print("\n⚠️ Continuando sin datos iniciales...")
    except FileNotFoundError:
        print("❌ No se encontró el script scripts/init_db.py")
        print("⚠️ Continuando sin inicializar la base de datos...")

def run_server():
    """Inicia el servidor FastAPI"""
    print("\n🏥 Iniciando Sistema de Monitoreo de Pacientes")
    print("📡 API disponible en: http://localhost:8001")
    print("📚 Documentación en: http://localhost:8001/docs")
    print("🔄 Modo desarrollo: Activado (reinicio automático)")
    print("⚡ Generación automática de datos: Activa")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,
        reload_dirs=["app/"]
    )

if __name__ == "__main__":
    # Verificar servicios Docker primero
    if not check_docker_services():
        print("\n⚠️ Algunos servicios no están disponibles. Continuando...")
        time.sleep(2)
    
    # Ejecutar inicialización de la base de datos
    run_init_db()
    
    # Pequeña pausa para que los mensajes sean legibles
    time.sleep(1)
    
    # Iniciar el servidor
    run_server()
