"""
Aplicación principal USICAMM
"""

import tkinter as tk
from tkinter import messagebox
import logging

from config import COLOR_FONDO, FUENTE_TITULO, LOG_FILE
from database import DatabaseManager
from logic import ExamenEngine
from security import SecurityMonitor, ValidadorCURP
from ui import PantallaCURP, PantallaTerminos, PantallaExamen, PantallaResultados
from pdf_generator import PDFGenerator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class AplicacionUSICAMM:
    """Aplicación principal"""

    def __init__(self, root):
        self.root = root
        self.root.title("USICAMM - Sistema de Examen")
        self.root.geometry("950x750")
        self.root.config(bg=COLOR_FONDO)

        # Inicializar componentes
        self.db = DatabaseManager()
        self.engine = None
        self.monitor = SecurityMonitor(
            callback_advertencia=self.on_advertencia,
            callback_fraude=self.on_fraude
        )
        self.validador = ValidadorCURP()
        self.pdf_generator = PDFGenerator()

        self.datos_aspirante = None
        self.sesion_activa = False
        self.timer_id = None

        logger.info("✅ Aplicación iniciada")
        self.mostrar_pantalla_inicial()

    def mostrar_pantalla_inicial(self):
        """Mostrar pantalla inicial"""
        self.limpiar_ventana()

        tk.Label(
            self.root,
            text="USICAMM",
            font=("Arial", 40, "bold"),
            bg=COLOR_FONDO,
            fg="#1E40AF"
        ).pack(pady=30)

        tk.Label(
            self.root,
            text="Bienvenido al Sistema de Examen\n\n¡Esperamos éxito en tu evaluación!",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO,
            justify=tk.CENTER
        ).pack(pady=30)

        tk.Button(
            self.root,
            text="INICIAR SESIÓN",
            command=self.iniciar_ingreso,
            font=("Arial", 14, "bold"),
            bg="#1E40AF",
            fg="white",
            padx=30,
            pady=15
        ).pack(pady=30)

    def iniciar_ingreso(self):
        """Iniciar ingreso"""
        PantallaCURP(self.root, self.validar_curp)

    def validar_curp(self, curp: str):
        """Validar CURP"""
        if not self.validador.validar_formato(curp):
            messagebox.showerror("Error", "Formato de CURP inválido")
            self.mostrar_pantalla_inicial()
            return

        datos = self.db.validar_aspirante(curp)
        if not datos:
            messagebox.showerror("Error", "CURP no encontrado")
            self.mostrar_pantalla_inicial()
            return

        self.datos_aspirante = datos
        PantallaTerminos(self.root, self.aceptar_terminos)

    def aceptar_terminos(self):
        """Aceptar términos"""
        self.engine = ExamenEngine(self.db)
        self.engine.preparar_examen(self.datos_aspirante)
        self.engine.iniciar_examen()
        self.sesion_activa = True
        self.monitor.iniciar()
        self.mostrar_examen()

    def mostrar_examen(self):
        """Mostrar examen"""
        progreso = self.engine.obtener_progreso()
        if not progreso.get('pregunta'):
            self.finalizar_examen()
            return

        self.limpiar_ventana()
        PantallaExamen(self.root, self.engine, self.siguiente_pantalla)
        self.actualizar_cronometro()

    def siguiente_pantalla(self, finalizar=False):
        """Siguiente pantalla"""
        if finalizar or not self.engine.avanzar_pregunta():
            self.finalizar_examen()
        else:
            self.mostrar_examen()

    def actualizar_cronometro(self):
        """Actualizar cronómetro"""
        if not self.sesion_activa:
            return

        if self.engine.timeout_examen():
            self.sesion_activa = False
            messagebox.showwarning("Tiempo Agotado", "Se acabó el tiempo")
            self.finalizar_examen()

        self.timer_id = self.root.after(1000, self.actualizar_cronometro)

    def finalizar_examen(self):
        """Finalizar examen"""
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        self.sesion_activa = False
        self.monitor.detener()
        resultado = self.engine.finalizar_examen()

        self.limpiar_ventana()
        PantallaResultados(
            self.root,
            resultado,
            lambda: self.descargar_pdf(resultado)
        )

    def descargar_pdf(self, resultado):
        """Descargar PDF"""
        ruta = self.pdf_generator.generar_pdf_conclusion(resultado)
        if ruta:
            messagebox.showinfo("Éxito", f"Comprobante guardado en:\n{ruta}")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "No se pudo generar el comprobante")

    def on_advertencia(self, evento):
        """Callback advertencia"""
        messagebox.showwarning(
            f"Advertencia {evento.get('numero')}/5",
            evento.get('razon')
        )

    def on_fraude(self, evento):
        """Callback fraude"""
        self.sesion_activa = False
        self.monitor.detener()
        self.engine.cancelar_examen(evento.get('razon'))
        messagebox.showerror("Fraude Detectado", "El examen ha sido cancelado.")
        self.root.destroy()

    def limpiar_ventana(self):
        """Limpiar ventana"""
        for widget in self.root.winfo_children():
            widget.destroy()

    def on_closing(self):
        """Cerrar aplicación"""
        if messagebox.askyesno("Salir", "¿Desea cerrar?"):
            self.monitor.detener()
            self.db.cerrar()
            self.root.destroy()


def main():
    """Función principal"""
    root = tk.Tk()
    app = AplicacionUSICAMM(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    logger.info("🚀 USICAMM iniciada")
    root.mainloop()


if __name__ == "__main__":
    main()