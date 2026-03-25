import arcade
# Para la ventana
from constants import *

class GameOverView(arcade.View):
    """Pantalla de fin de juego"""
    def __init__(self, final_score):
        super().__init__()
        self.final_score = final_score

        self.background_sprite_list = arcade.SpriteList()

        # Background
        background = "assets/images/background/background1/orig_big.png"
        self.backgroung_img = arcade.Sprite(background, scale=0.6, center_x=WINDOW_WIDTH / 2,
                                            center_y=WINDOW_HEIGHT / 2)
        self.background_sprite_list.append(self.backgroung_img)

        self.start_x = WINDOW_WIDTH / 2
        self.start_y = WINDOW_HEIGHT / 2

        self.text_game_over = arcade.Text(
            text="GAME OVER",
            x=self.start_x, y=self.start_y + DEFAULT_LINE_HEIGHT,
            color=arcade.color.RED_DEVIL,
            font_size=50,
            font_name="Kenney Pixel Square",
            anchor_x="center",
            anchor_y="baseline",
        )

        self.text_score = arcade.Text(
            text=f"Tu puntuación: {self.final_score}",
            x=self.start_x, y=self.start_y - DEFAULT_LINE_HEIGHT,
            color=arcade.color.YELLOW,
            font_size=DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )

        self.text_main_window = arcade.Text(
            text="Pulsa cualquier tecla para volver al menú...",
            x=self.start_x, y=self.start_y - DEFAULT_LINE_HEIGHT * 1.5,
            color=arcade.color.WHITE,
            font_size=DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BATTLESHIP_GREY)
        if self.final_score > self.window.high_score:
            self.window.high_score = self.final_score

    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw()

        self.text_game_over.draw()
        self.text_score.draw()
        self.text_main_window.draw()

    def on_key_press(self, symbol, modifiers):
        from main import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
