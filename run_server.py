"""
Script para ejecutar el servidor de desarrollo
"""

import subprocess
import sys
import time
import uvicorn
from app.main import app

def run_init_db():
    """Ejecuta el script de inicialización de la base de datos"""
    print("\n🔍 Verificando estado de la base de datos...")
    try:
        # Ejecutar el script de inicialización
        result = subprocess.run(
            [sys.executable, "scripts/init_db.py"],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Mostrar salida del script
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
        reload_dirs=["app/"]  # Monitorea cambios en toda la carpeta app
    )

if __name__ == "__main__":
    # Ejecutar inicialización de la base de datos primero
    run_init_db()
    
    # Pequeña pausa para que los mensajes sean legibles
    time.sleep(1)
    
    # Iniciar el servidor
    run_server()
