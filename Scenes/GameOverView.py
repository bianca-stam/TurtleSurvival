import arcade
# Para la ventana
from constants import *

class GameOverView(arcade.View):
    """Pantalla de fin de juego"""
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
        if self.final_score > self.window.high_score:
            self.window.high_score = self.final_score

    def on_draw(self):
        self.clear()
        arcade.draw_text("GAME OVER", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.6,
                         arcade.color.RED_DEVIL, font_size=50, anchor_x="center")

        arcade.draw_text(f"Tu puntuación: {self.final_score}", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.4,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        arcade.draw_text("Pulsa cualquier tecla para volver al menú", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.2,
                         arcade.color.WHITE, font_size=15, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        from main import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
