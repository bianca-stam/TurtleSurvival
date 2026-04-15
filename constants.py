import os
import sys
from pathlib import Path
import arcade

if getattr(sys, 'frozen', False):
    # Si es un ejecutable, sys._MEIPASS apunta automáticamente
    # a la carpeta donde están los datos (ya sea la raíz o _internal)
    ROOT_DIR = Path(sys._MEIPASS).resolve()
else:
    # Si estamos en modo desarrollo (PyCharm)
    ROOT_DIR = Path(__file__).parent.resolve()

# Definimos la carpeta de assets relativa a esa raíz detectada
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")

# Registramos el handle
arcade.resources.add_resource_handle("assets", ASSETS_DIR)

# --- Configuración de la Ventana ---
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
WINDOW_TITLE = "FishyFishy"

# --- Estilos de Texto y Fuentes ---
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20
arcade.resources.load_kenney_fonts()
arcade.resources.load_liberation_fonts()

# --- Mecánicas de Movimiento ---
PLAYER_MOVEMENT_SPEED = 100
MOB_MOVEMENT_SPEED = 200
SPAWN_INTERVAL = 0.5  # segundos entre cada enemigo

# --- Lógica de Juego y Puntuación ---
POINTS_PER_SECOND = 1

# --- Rutas para todas las imágenes ---
# Esto le dice a Arcade que busque dentro de tu carpeta 'assets'
