"""
Componentes de interfaz gráfica para USICAMM
"""

import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_BLANCO,
    FUENTE_TITULO, FUENTE_NORMAL, TERMINOS_Y_CONDICIONES,
    REGLAS_APLICACION
)


class PantallaCURP:
    """Pantalla de ingreso de CURP"""

    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.mostrar()

    def mostrar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        frame = tk.Frame(self.root, bg=COLOR_BLANCO)
        frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, width=400, height=250)

        tk.Label(
            frame,
            text="INGRESE SU CURP",
            font=FUENTE_TITULO,
            bg=COLOR_BLANCO
        ).pack(pady=20)

        tk.Label(
            frame,
            text="Clave Única de Registro de Población",
            font=FUENTE_NORMAL,
            bg=COLOR_BLANCO
        ).pack(pady=5)

        self.entry = tk.Entry(frame, font=("Arial", 14), width=25)
        self.entry.pack(pady=15)
        self.entry.focus()

        tk.Button(
            frame,
            text="CONTINUAR",
            command=self.validar,
            font=("Arial", 12, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO,
            padx=30,
            pady=10
        ).pack(pady=15)

    def validar(self):
        curp = self.entry.get().upper().strip()
        if len(curp) != 18:
            messagebox.showerror("Error", "El CURP debe tener 18 caracteres")
            return
        self.callback(curp)


class PantallaTerminos:
    """Pantalla de términos y condiciones"""

    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        self.mostrar()

    def mostrar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="TÉRMINOS Y CONDICIONES",
            font=FUENTE_TITULO,
            bg=COLOR_FONDO
        ).pack(pady=10)

        frame_texto = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_texto.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(frame_texto)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        texto = tk.Text(
            frame_texto,
            height=15,
            width=80,
            yscrollcommand=scrollbar.set,
            font=("Arial", 10)
        )
        texto.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=texto.yview)

        texto.insert(tk.END, TERMINOS_Y_CONDICIONES)
        texto.insert(tk.END, "\n\n" + REGLAS_APLICACION)
        texto.config(state=tk.DISABLED)

        self.var_acepta = tk.BooleanVar()
        tk.Checkbutton(
            self.root,
            text="Acepto los términos y condiciones",
            variable=self.var_acepta,
            font=FUENTE_NORMAL,
            bg=COLOR_FONDO
        ).pack(pady=10)

        frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        tk.Button(
            frame_botones,
            text="RECHAZAR",
            command=self.root.destroy,
            font=("Arial", 11),
            bg="#EF4444",
            fg=COLOR_BLANCO,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            frame_botones,
            text="ACEPTAR",
            command=self.aceptar,
            font=("Arial", 11),
            bg="#10B981",
            fg=COLOR_BLANCO,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

    def aceptar(self):
        if not self.var_acepta.get():
            messagebox.showwarning(
                "Requerido",
                "Debe aceptar los términos y condiciones"
            )
            return
        self.callback()


class PantallaExamen:
    """Pantalla del examen"""

    def __init__(self, root, engine, callback_siguiente):
        self.root = root
        self.engine = engine
        self.callback_siguiente = callback_siguiente
        self.var_respuesta = tk.StringVar()
        self.mostrar()

    def mostrar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        progreso = self.engine.obtener_progreso()
        pregunta = progreso.get('pregunta')

        # Header
        frame_header = tk.Frame(self.root, bg=COLOR_PRIMARIO)
        frame_header.pack(fill=tk.X, pady=10)

        tk.Label(
            frame_header,
            text=f"⏱️ {progreso['tiempo_restante']}",
            font=("Arial", 16, "bold"),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        ).pack(side=tk.LEFT, padx=20, pady=10)

        tk.Label(
            frame_header,
            text=f"Pregunta {progreso['pregunta_actual']}/{progreso['total_preguntas']}",
            font=("Arial", 12),
            bg=COLOR_PRIMARIO,
            fg=COLOR_BLANCO
        ).pack(side=tk.RIGHT, padx=20, pady=10)

        # Pregunta
        tk.Label(
            self.root,
            text=pregunta.get('pregunta', ''),
            font=("Arial", 14),
            bg=COLOR_FONDO,
            wraplength=800,
            justify=tk.LEFT
        ).pack(padx=20, pady=20)

        # Opciones
        frame_opciones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_opciones.pack(padx=50, pady=10)

        for opcion in pregunta.get('opciones', []):
            tk.Radiobutton(
                frame_opciones,
                text=opcion,
                variable=self.var_respuesta,
                value=opcion,
                font=("Arial", 12),
                bg=COLOR_FONDO
            ).pack(anchor=tk.W, pady=5)

        # Botones
        frame_botones = tk.Frame(self.root, bg=COLOR_FONDO)
        frame_botones.pack(pady=20)

        tk.Button(
            frame_botones,
            text="SIGUIENTE",
            command=self.siguiente,
            font=("Arial", 11),
            bg="#1E40AF",
            fg=COLOR_BLANCO,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

        tk.Button(
            frame_botones,
            text="FINALIZAR",
            command=self.finalizar,
            font=("Arial", 11),
            bg="#10B981",
            fg=COLOR_BLANCO,
            padx=20,
            pady=8
        ).pack(side=tk.LEFT, padx=10)

    def siguiente(self):
        respuesta = self.var_respuesta.get()
        if respuesta:
            self.engine.guardar_respuesta_actual(respuesta)
            self.callback_siguiente()
        else:
            messagebox.showwarning(
                "Seleccione",
                "Debe seleccionar una respuesta"
            )

    def finalizar(self):
        if messagebox.askyesno("Confirmar", "¿Desea finalizar el examen?"):
            respuesta = self.var_respuesta.get()
            if respuesta:
                self.engine.guardar_respuesta_actual(respuesta)
            self.callback_siguiente(finalizar=True)


class PantallaResultados:
    """Pantalla de resultados"""

    def __init__(self, root, resultado, callback_descarga):
        self.root = root
        self.resultado = resultado
        self.callback_descarga = callback_descarga
        self.mostrar()

    def mostrar(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(
            self.root,
            text="¡EXAMEN CONCLUIDO!",
            font=("Arial", 28, "bold"),
            bg=COLOR_FONDO,
            fg=COLOR_PRIMARIO
        ).pack(pady=30)

        tk.Label(
            self.root,
            text="Gracias por su participación",
            font=FUENTE_NORMAL,
            bg=COLOR_FONDO
        ).pack(pady=10)

        # Resultados
        frame_resultados = tk.Frame(self.root, bg=COLOR_BLANCO, relief=tk.RAISED, bd=2)
        frame_resultados.pack(padx=50, pady=20, fill=tk.BOTH)

        puntuacion = self.resultado.get('puntuacion', 0)
        porcentaje = self.resultado.get('porcentaje_acierto', 0)

        tk.Label(
            frame_resultados,
            text=f"Puntuación: {puntuacion}/100",
            font=("Arial", 16, "bold"),
            bg=COLOR_BLANCO
        ).pack(pady=10)

        tk.Label(
            frame_resultados,
            text=f"Porcentaje de acierto: {porcentaje:.1f}%",
            font=("Arial", 14),
            bg=COLOR_BLANCO
        ).pack(pady=5)

        tk.Label(
            frame_resultados,
            text=f"Preguntas correctas: {self.resultado.get('preguntas_correctas', 0)}/{self.resultado.get('preguntas_totales', 0)}",
            font=("Arial", 14),
            bg=COLOR_BLANCO
        ).pack(pady=5)

        tk.Button(
            self.root,
            text="DESCARGAR COMPROBANTE PDF",
            command=self.callback_descarga,
            font=("Arial", 12, "bold"),
            bg="#10B981",
            fg=COLOR_BLANCO,
            padx=30,
            pady=15
        ).pack(pady=30)