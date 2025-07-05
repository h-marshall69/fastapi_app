"""
Script para ejecutar el servidor de desarrollo
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🏥 Iniciando Sistema de Monitoreo de Pacientes")
    print("📡 API disponible en: http://localhost:8000")
    print("📚 Documentación en: http://localhost:8000/docs")
    print("🔄 Generación automática de datos: Activa")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True,  # Reinicia automáticamente en desarrollo
        reload_dirs=["localhost/"]  # Directorio a monitorear
    )


