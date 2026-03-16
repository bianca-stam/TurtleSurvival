import arcade
from constants import *

class MenuView(arcade.View):
    """Pantalla principal de inicio"""
    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        high_score = self.window.high_score

        arcade.draw_text("MI SUPER JUEGO", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.7,
                         arcade.color.WHITE, font_size=40, anchor_x="center")

        arcade.draw_text(f"Puntuación Máxima: {high_score}", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.5,
                         arcade.color.GOLD, font_size=20, anchor_x="center")

        arcade.draw_text("Pulsa cualquier tecla para empezar", WINDOW_WIDTH / 2, WINDOW_HEIGHT * 0.3,
                         arcade.color.LIGHT_GRAY, font_size=15, anchor_x="center")

    def on_key_press(self, symbol, modifiers):
        # Al pulsar cualquier tecla, vamos al juego
        from Scenes.MainGameView import GameView
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
