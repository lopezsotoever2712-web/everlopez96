"""
Script de configuración de base de datos
"""

import logging
from database import DatabaseManager
from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def setup():
    """Configurar base de datos"""
    try:
        logger.info("🔧 Inicializando base de datos...")
        db = DatabaseManager()
        logger.info("✅ Base de datos configurada correctamente")
        db.cerrar()

    except Exception as e:
        logger.error(f"❌ Error en configuración: {e}")


if __name__ == "__main__":
    setup()