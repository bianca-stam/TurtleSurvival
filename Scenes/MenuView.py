import arcade
from constants import *

class MenuView(arcade.View):
    """Pantalla principal de inicio"""
    def __init__(self):
        super().__init__()
        # Add the screen title
        self.start_x = WINDOW_WIDTH / 2
        self.start_y = WINDOW_HEIGHT / 2

        self.text_main_title = arcade.Text(
            text="Turtle Survival",
            x=self.start_x, y=self.start_y + DEFAULT_LINE_HEIGHT,
            color=arcade.color.BLACK,
            font_size=50,
            font_name="Kenney Pixel Square",
            anchor_x="center",
            anchor_y="baseline",
        )

        self.start_text = arcade.Text(
            text="Pulse cualquier tecla para empezar...",
            x=self.start_x, y=self.start_y - DEFAULT_LINE_HEIGHT * 1.5,
            color=arcade.color.YELLOW,
            font_size=DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )

        self.background_sprite_list = arcade.SpriteList()

        # Background
        background = "assets/images/background/background1/orig_big.png"
        self.backgroung_img = arcade.Sprite(background, scale=0.6, center_x=WINDOW_WIDTH / 2,
                                            center_y=WINDOW_HEIGHT / 2)
        self.background_sprite_list.append(self.backgroung_img)


    def on_show_view(self):
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw()

        high_score = self.window.high_score

        self.score_text = arcade.Text(
            text=f"Puntuación Máxima: {high_score}",
            x=self.start_x, y=self.start_y + 20,
            color=arcade.color.BLACK,
            font_size=DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )

        self.score_text.draw()

        self.text_main_title.draw()
        self.start_text.draw()


    def on_key_press(self, symbol, modifiers):
        # Al pulsar cualquier tecla, vamos al juego
        from Scenes.MainGameView import GameView
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
