"""
Punto de entrada principal de la aplicación.

Este módulo inicializa la ventana del juego con la librería Arcade,
configura el estado global (como la puntuación máxima) y lanza
la vista del menú principal.
"""

from Scenes.MenuView import MenuView
from constants import *

def main() -> None:
    """Inicializa y ejecuta el bucle principal del juego.

    Crea la ventana de Arcade con las dimensiones y título definidos
    en las constantes globales, establece la puntuación máxima inicial
    en cero, centra la ventana en pantalla y arranca la vista del menú.

    Returns:
        None

    Example:
        Para lanzar el juego directamente desde consola::

            $ python main.py
    """

    window = arcade.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
    window.high_score = 0
    window.center_window()

    game = MenuView()
    window.show_view(game)
    arcade.run()

if __name__ == "__main__":
    main()
