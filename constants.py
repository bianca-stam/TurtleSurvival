import arcade

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
WINDOW_TITLE = "FishyFishy"

# Para el texto
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20
arcade.resources.load_kenney_fonts()
arcade.resources.load_liberation_fonts()

# Para el movimiento
PLAYER_MOVEMENT_SPEED = 100
MOB_MOVEMENT_SPEED = 200
SPAWN_INTERVAL = 0.5  # segundos entre cada enemigo

# Estadísticas de la partida
POINTS_PER_SECOND = 1