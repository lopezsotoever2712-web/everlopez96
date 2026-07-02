"""
Temas y estilos mejorados para interfaz
"""

from config import (
    COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_EXITOSO,
    COLOR_ADVERTENCIA, COLOR_ERROR, COLOR_FONDO,
    COLOR_BLANCO, COLOR_TEXTO
)

# Tema claro (default)
TEMA_CLARO = {
    "primario": COLOR_PRIMARIO,
    "secundario": COLOR_SECUNDARIO,
    "exitoso": COLOR_EXITOSO,
    "advertencia": COLOR_ADVERTENCIA,
    "error": COLOR_ERROR,
    "fondo": COLOR_FONDO,
    "blanco": COLOR_BLANCO,
    "texto": COLOR_TEXTO,
}

# Tema oscuro
TEMA_OSCURO = {
    "primario": "#0F3460",
    "secundario": "#533483",
    "exitoso": "#06A77D",
    "advertencia": "#D8941F",
    "error": "#D62828",
    "fondo": "#1A1A2E",
    "blanco": "#16213E",
    "texto": "#E0E0E0",
}

# Estilos de botones
ESTILOS_BOTON = {
    "primario": {
        "bg": COLOR_PRIMARIO,
        "fg": COLOR_BLANCO,
        "activebackground": COLOR_SECUNDARIO,
        "activeforeground": COLOR_BLANCO,
        "relief": "raised",
        "bd": 2,
        "padx": 20,
        "pady": 10,
        "font": ("Arial", 11, "bold")
    },
    "secundario": {
        "bg": COLOR_SECUNDARIO,
        "fg": COLOR_BLANCO,
        "activebackground": COLOR_PRIMARIO,
        "activeforeground": COLOR_BLANCO,
        "relief": "raised",
        "bd": 2,
        "padx": 20,
        "pady": 10,
        "font": ("Arial", 11, "bold")
    },
    "exitoso": {
        "bg": COLOR_EXITOSO,
        "fg": COLOR_BLANCO,
        "activebackground": COLOR_PRIMARIO,
        "activeforeground": COLOR_BLANCO,
        "relief": "raised",
        "bd": 2,
        "padx": 20,
        "pady": 10,
        "font": ("Arial", 11, "bold")
    },
    "error": {
        "bg": COLOR_ERROR,
        "fg": COLOR_BLANCO,
        "activebackground": COLOR_ADVERTENCIA,
        "activeforeground": COLOR_BLANCO,
        "relief": "raised",
        "bd": 2,
        "padx": 20,
        "pady": 10,
        "font": ("Arial", 11, "bold")
    }
}
