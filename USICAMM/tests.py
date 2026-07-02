"""
Suite de pruebas para USICAMM
"""

import unittest
from datetime import datetime
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))

from config import NUM_PREGUNTAS, DURACION_EXAMEN
from security import ValidadorCURP
from logic import ExamenEngine
from database import DatabaseManager


class TestValidadorCURP(unittest.TestCase):
    """Tests para ValidadorCURP"""

    def setUp(self):
        self.validador = ValidadorCURP()

    def test_validar_formato_correcto(self):
        """Probar formato CURP correcto"""
        curp_valido = "ABCD930315HDFRNS09"
        self.assertTrue(self.validador.validar_formato(curp_valido))

    def test_validar_formato_incorrecto_longitud(self):
        """Probar formato CURP con longitud incorrecta"""
        curp_invalido = "ABCD930315HDFR"
        self.assertFalse(self.validador.validar_formato(curp_invalido))

    def test_validar_fecha_valida(self):
        """Probar validación de fecha válida"""
        curp = "ABCD930315HDFRNS09"
        self.assertTrue(self.validador.validar_fecha(curp))


class TestExamenEngine(unittest.TestCase):
    """Tests para ExamenEngine"""

    def setUp(self):
        self.db = DatabaseManager()
        self.engine = ExamenEngine(self.db)
        
        self.datos_aspirante = {
            'id': 1,
            'curp': 'ABCD930315HDFRNS09',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez'
        }

    def tearDown(self):
        self.db.cerrar()

    def test_preparar_examen(self):
        """Probar preparación de examen"""
        self.engine.preparar_examen(self.datos_aspirante)
        self.assertEqual(len(self.engine.preguntas), NUM_PREGUNTAS)
        self.assertEqual(self.engine.estado, 'no_iniciado')

    def test_iniciar_examen(self):
        """Probar iniciar examen"""
        self.engine.preparar_examen(self.datos_aspirante)
        sesion_id = self.engine.iniciar_examen()
        
        self.assertGreater(sesion_id, 0)
        self.assertEqual(self.engine.estado, 'iniciado')
        self.assertIsNotNone(self.engine.inicio_examen)

    def test_avanzar_pregunta(self):
        """Probar avanzar entre preguntas"""
        self.engine.preparar_examen(self.datos_aspirante)
        self.engine.numero_pregunta_actual = 1
        
        resultado = self.engine.avanzar_pregunta()
        self.assertTrue(resultado)
        self.assertEqual(self.engine.numero_pregunta_actual, 2)

    def test_calcular_tiempo_restante(self):
        """Probar cálculo de tiempo restante"""
        self.engine.preparar_examen(self.datos_aspirante)
        self.engine.iniciar_examen()
        
        tiempo = self.engine.calcular_tiempo_restante()
        self.assertLessEqual(tiempo, DURACION_EXAMEN * 60)
        self.assertGreater(tiempo, 0)


class TestDatabaseManager(unittest.TestCase):
    """Tests para DatabaseManager"""

    def setUp(self):
        self.db = DatabaseManager()

    def tearDown(self):
        self.db.cerrar()

    def test_base_datos_inicializada(self):
        """Probar que la BD se inicializa correctamente"""
        self.assertIsNotNone(self.db.conexion)
        self.assertTrue(self.db.db_path.exists())


class TestIntegracion(unittest.TestCase):
    """Tests de integración"""

    def setUp(self):
        self.db = DatabaseManager()
        self.engine = ExamenEngine(self.db)
        self.validador = ValidadorCURP()
        
        self.datos_aspirante = {
            'id': 1,
            'curp': 'ABCD930315HDFRNS09',
            'nombre': 'Juan',
            'apellido_paterno': 'Pérez'
        }

    def tearDown(self):
        self.db.cerrar()

    def test_flujo_completo_examen(self):
        """Probar flujo completo de examen"""
        self.assertTrue(self.validador.validar_formato(self.datos_aspirante['curp']))
        self.engine.preparar_examen(self.datos_aspirante)
        self.assertGreater(len(self.engine.preguntas), 0)
        
        sesion_id = self.engine.iniciar_examen()
        self.assertGreater(sesion_id, 0)


if __name__ == "__main__":
    unittest.main()
