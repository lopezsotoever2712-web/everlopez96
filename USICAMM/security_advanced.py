"""
Sistema avanzado de seguridad con monitoreo en tiempo real
"""

import os
import sys
import json
import logging
import threading
import time
from typing import List, Dict, Optional
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None

from config import (
    PROCESOS_PROHIBIDOS, PALABRAS_CLAVE_PROHIBIDAS,
    MAX_ADVERTENCIAS, LOG_FILE, AUDIT_LOG_FILE
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)
audit_logger = logging.getLogger("audit")
audit_handler = logging.FileHandler(AUDIT_LOG_FILE)
audit_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
audit_logger.addHandler(audit_handler)
audit_logger.setLevel(logging.INFO)


class MonitorAvanzado:
    """Monitor avanzado de seguridad"""

    def __init__(self, callback_advertencia=None, callback_fraude=None):
        self.callback_advertencia = callback_advertencia
        self.callback_fraude = callback_fraude
        self.activo = False
        self.thread = None
        self.advertencias = []
        self.eventos = []
        self.ventana_activa_anterior = None
        self.dispositivos_detectados = set()

    def iniciar(self):
        """Iniciar monitoreo"""
        self.activo = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        logger.info("✅ Monitor avanzado iniciado")

    def detener(self):
        """Detener monitoreo"""
        self.activo = False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info("✅ Monitor detenido")

    def _monitor_loop(self):
        """Loop de monitoreo"""
        while self.activo:
            try:
                if psutil:
                    self._verificar_procesos()
                    self._verificar_alt_tab()
                    self._verificar_dispositivos()
                time.sleep(2)
            except Exception as e:
                logger.debug(f"Error en monitor: {e}")
                time.sleep(2)

    def _verificar_procesos(self):
        """Verificar procesos prohibidos"""
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                nombre = proc.info['name'].lower()
                for prohibido in PROCESOS_PROHIBIDOS:
                    if prohibido.lower() in nombre:
                        self._generar_advertencia(
                            "Proceso prohibido detectado",
                            [proc.info['name']]
                        )
                        return
        except:
            pass

    def _verificar_alt_tab(self):
        """Verificar cambios de ventana"""
        try:
            if sys.platform == "win32":
                import subprocess
                resultado = subprocess.run(
                    ["tasklist"],
                    capture_output=True,
                    text=True
                )
                ventanas = resultado.stdout.lower()
                
                for palabra in PALABRAS_CLAVE_PROHIBIDAS:
                    if palabra.lower() in ventanas:
                        self._generar_advertencia(
                            "Ventana prohibida detectada",
                            [palabra]
                        )
                        return
        except:
            pass

    def _verificar_dispositivos(self):
        """Verificar dispositivos conectados"""
        try:
            if sys.platform == "win32":
                import subprocess
                resultado = subprocess.run(
                    ["wmic", "logicaldisk", "get", "name"],
                    capture_output=True,
                    text=True
                )
                discos = resultado.stdout
                nuevos_discos = set(discos.split())
                
                diferencia = nuevos_discos - self.dispositivos_detectados
                if diferencia:
                    self._generar_advertencia(
                        "Dispositivo USB conectado",
                        list(diferencia)
                    )
                
                self.dispositivos_detectados = nuevos_discos
        except:
            pass

    def _generar_advertencia(self, razon: str, detalles: List[str]):
        """Generar advertencia"""
        evento = {
            "timestamp": datetime.now().isoformat(),
            "razon": razon,
            "detalles": detalles,
            "numero": len(self.advertencias) + 1
        }
        
        self.advertencias.append(evento)
        logger.warning(f"⚠️ ADVERTENCIA {evento['numero']}/5 - {razon}")
        audit_logger.warning(f"ADVERTENCIA - {razon}")
        
        if self.callback_advertencia:
            self.callback_advertencia(evento)
        
        if len(self.advertencias) >= MAX_ADVERTENCIAS:
            self._generar_fraude("Límite de advertencias alcanzado")

    def _generar_fraude(self, razon: str):
        """Generar fraude"""
        logger.critical(f"🚨 FRAUDE DETECTADO - {razon}")
        audit_logger.critical(f"FRAUDE_DETECTADO - {razon}")
        
        if self.callback_fraude:
            self.callback_fraude({
                "timestamp": datetime.now().isoformat(),
                "razon": razon,
                "advertencias": len(self.advertencias)
            })

    def obtener_reporte(self) -> Dict:
        """Obtener reporte de seguridad"""
        return {
            "timestamp": datetime.now().isoformat(),
            "advertencias_totales": len(self.advertencias),
            "eventos_totales": len(self.eventos),
            "advertencias": self.advertencias,
            "eventos": self.eventos
        }
