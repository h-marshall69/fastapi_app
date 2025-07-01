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
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Reinicia automáticamente en desarrollo
        reload_dirs=["./"]  # Directorio a monitorear
    )


