"""
Conexión a base de datos PostgreSQL central
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime
from config import LOG_FILE

logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class DatabaseCentral:
    """Gestor de base de datos central PostgreSQL"""

    def __init__(self):
        self.conexion = None
        self.inicializar()

    def inicializar(self):
        """Inicializar conexión"""
        try:
            import psycopg2
            
            from config import DB_CENTRAL_CONFIG
            
            self.conexion = psycopg2.connect(
                host=DB_CENTRAL_CONFIG['host'],
                port=DB_CENTRAL_CONFIG['port'],
                user=DB_CENTRAL_CONFIG['user'],
                password=DB_CENTRAL_CONFIG['password'],
                database=DB_CENTRAL_CONFIG['database']
            )
            
            logger.info("✅ Conectado a BD Central PostgreSQL")
            self.crear_tablas()
            
        except ImportError:
            logger.warning("⚠️ psycopg2 no instalado - BD central no disponible")
        except Exception as e:
            logger.warning(f"⚠️ No se pudo conectar a BD Central: {e}")

    def crear_tablas(self):
        """Crear tablas en BD central"""
        if not self.conexion:
            return
        
        try:
            cursor = self.conexion.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resultados_finales (
                    id SERIAL PRIMARY KEY,
                    curp VARCHAR(18) UNIQUE NOT NULL,
                    nombre VARCHAR(100),
                    puntuacion DECIMAL(5,2),
                    porcentaje_acierto DECIMAL(5,2),
                    preguntas_correctas INTEGER,
                    preguntas_totales INTEGER,
                    fecha_examen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    sincronizado_local BOOLEAN DEFAULT FALSE
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS auditoria_completa (
                    id SERIAL PRIMARY KEY,
                    tipo_evento VARCHAR(50),
                    descripcion TEXT,
                    curp VARCHAR(18),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            self.conexion.commit()
            logger.info("✅ Tablas creadas en BD Central")
            
        except Exception as e:
            logger.error(f"❌ Error al crear tablas: {e}")

    def guardar_resultado(self, resultado: Dict) -> bool:
        """Guardar resultado en BD central"""
        if not self.conexion:
            return False
        
        try:
            cursor = self.conexion.cursor()
            
            cursor.execute('''
                INSERT INTO resultados_finales 
                (curp, nombre, puntuacion, porcentaje_acierto, 
                 preguntas_correctas, preguntas_totales)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                resultado.get('curp'),
                resultado.get('nombre_aspirante'),
                resultado.get('puntuacion'),
                resultado.get('porcentaje_acierto'),
                resultado.get('preguntas_correctas'),
                resultado.get('preguntas_totales')
            ))
            
            self.conexion.commit()
            logger.info(f"✅ Resultado guardado en BD Central: {resultado.get('curp')}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error al guardar resultado: {e}")
            return False

    def obtener_listado_nominal(self, ordenar_por='puntuacion', limite=100) -> List[Dict]:
        """Obtener listado nominal ordenado"""
        if not self.conexion:
            return []
        
        try:
            cursor = self.conexion.cursor()
            
            query = f'''
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY {ordenar_por} DESC) as posicion,
                    curp, nombre, puntuacion, porcentaje_acierto,
                    preguntas_correctas, preguntas_totales, fecha_examen
                FROM resultados_finales
                ORDER BY {ordenar_por} DESC
                LIMIT %s
            '''
            
            cursor.execute(query, (limite,))
            
            resultados = []
            for row in cursor.fetchall():
                resultados.append({
                    'posicion': row[0],
                    'curp': row[1],
                    'nombre': row[2],
                    'puntuacion': float(row[3]),
                    'porcentaje_acierto': float(row[4]),
                    'preguntas_correctas': row[5],
                    'preguntas_totales': row[6],
                    'fecha_examen': row[7].isoformat() if row[7] else None
                })
            
            return resultados
            
        except Exception as e:
            logger.error(f"❌ Error al obtener listado nominal: {e}")
            return []

    def cerrar(self):
        """Cerrar conexión"""
        if self.conexion:
            try:
                self.conexion.close()
                logger.info("✅ Conexión a BD Central cerrada")
            except Exception as e:
                logger.error(f"❌ Error al cerrar conexión: {e}")

    def __del__(self):
        self.cerrar()
