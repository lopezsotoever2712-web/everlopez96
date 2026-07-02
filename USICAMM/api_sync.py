"""
API REST para sincronización con base de datos central
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from datetime import datetime

from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)


class APISincronizacion:
    """API de sincronización"""

    def __init__(self, db):
        self.db = db
        self.registrar_rutas()

    def registrar_rutas(self):
        """Registrar rutas API"""

        @app.route('/api/v1/health', methods=['GET'])
        def health():
            """Verificar estado del servidor"""
            return jsonify({
                "status": "ok",
                "timestamp": datetime.now().isoformat()
            }), 200

        @app.route('/api/v1/aspirantes/validar', methods=['POST'])
        def validar_aspirante():
            """Validar aspirante"""
            try:
                data = request.json
                curp = data.get('curp', '')
                
                aspirante = self.db.validar_aspirante(curp)
                
                if aspirante:
                    return jsonify({
                        "success": True,
                        "datos": aspirante
                    }), 200
                else:
                    return jsonify({
                        "success": False,
                        "error": "CURP no encontrado"
                    }), 404
            except Exception as e:
                logger.error(f"Error al validar: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        @app.route('/api/v1/examenes/<int:sesion_id>/resultados', methods=['GET'])
        def obtener_resultados(sesion_id):
            """Obtener resultados de examen"""
            try:
                sesion = self.db.obtener_datos_sesion(sesion_id)
                
                if sesion:
                    return jsonify({
                        "success": True,
                        "sesion": sesion
                    }), 200
                else:
                    return jsonify({
                        "success": False,
                        "error": "Sesión no encontrada"
                    }), 404
            except Exception as e:
                logger.error(f"Error al obtener resultados: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        @app.route('/api/v1/sincronizar', methods=['POST'])
        def sincronizar():
            """Sincronizar datos"""
            try:
                data = request.json
                tipo_dato = data.get('tipo')
                
                logger.info(f"🔄 Sincronizando: {tipo_dato}")
                
                return jsonify({
                    "success": True,
                    "mensaje": f"Datos de {tipo_dato} sincronizados"
                }), 200
            except Exception as e:
                logger.error(f"Error al sincronizar: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        @app.route('/api/v1/listado-nominal', methods=['GET'])
        def obtener_listado_nominal():
            """Obtener listado nominal de resultados"""
            try:
                listado = [
                    {
                        "posicion": 1,
                        "curp": "ABCD930315HDFRNS09",
                        "nombre": "Juan Pérez",
                        "puntuacion": 95.5,
                        "fecha": datetime.now().isoformat()
                    }
                ]
                
                return jsonify({
                    "success": True,
                    "listado": listado
                }), 200
            except Exception as e:
                logger.error(f"Error al obtener listado: {e}")
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

    def ejecutar(self, host='0.0.0.0', puerto=5000, debug=False):
        """Ejecutar servidor"""
        app.run(host=host, port=puerto, debug=debug)
