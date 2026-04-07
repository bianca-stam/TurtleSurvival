import arcade

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