from constants import *

class GameOverView(arcade.View):
    """
    Vista que se muestra cuando el jugador pierde la partida.
    Muestra la puntuación final y permite regresar al menú principal.
    """
    def __init__(self, final_score):
        """
        Configura los elementos visuales de la pantalla de Game Over.

        Args:
            final_score (int): La puntuación alcanzada por el jugador antes de morir.
        """
        super().__init__()
        self.final_score = final_score
        self.background_sprite_list = arcade.SpriteList()

        # Background
        background = "assets/images/background/background1/orig_big.png"
        self.background_img = arcade.Sprite(background, scale=0.6, center_x=WINDOW_WIDTH / 2,
                                            center_y=WINDOW_HEIGHT / 2)
        self.background_sprite_list.append(self.background_img)

        self.start_x = WINDOW_WIDTH / 2
        self.start_y = WINDOW_HEIGHT / 2

        # Texto en la pantalla
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
        """Acciones a ejecutar cuando la ventana cambia a esta vista."""
        if self.final_score > self.window.high_score:
            self.window.high_score = self.final_score

    def on_draw(self):
        """Renderiza los elementos en pantalla."""
        self.clear()

        self.background_sprite_list.draw()

        self.text_game_over.draw()
        self.text_score.draw()
        self.text_main_window.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Escucha cualquier pulsación de tecla para regresar al menú.

        El 'import' se hace dentro para evitar importaciones circulares.
        """
        from main import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)
