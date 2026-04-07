"""
Módulo que contiene la vista del menú principal del juego.
"""

from constants import *

class MenuView(arcade.View):
    """Vista del menú principal que se muestra al arrancar el juego.

    Renderiza el título, el fondo, la puntuación máxima y un mensaje
    de inicio. Cualquier pulsación de tecla transiciona a la vista
    principal del juego.

    Attributes:
        start_x (float): Coordenada X central de la ventana.
        start_y (float): Coordenada Y central de la ventana.
        text_main_title (arcade.Text): Texto con el título "Turtle Survival".
        start_text (arcade.Text): Texto de instrucción para comenzar.
        background_sprite_list (arcade.SpriteList): Lista con el sprite de fondo.
        background_img (arcade.Sprite): Sprite de la imagen de fondo.
    """

    def __init__(self):
        """Inicializa la vista del menú y prepara todos sus elementos visuales.

        Calcula el centro de la ventana y construye los objetos de texto
        y sprites necesarios para renderizar el menú.
        """
        super().__init__()
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
        self.background_img = arcade.Sprite(background, scale=0.6, center_x=WINDOW_WIDTH / 2,
                                            center_y=WINDOW_HEIGHT / 2)
        self.background_sprite_list.append(self.background_img)


    def on_show_view(self):
        """Callback ejecutado cuando esta vista se convierte en la activa.

        Establece el color de fondo de la ventana.
        """
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self):
        """Renderiza todos los elementos visuales del menú en cada frame.

        Dibuja en orden: fondo, puntuación máxima, título y mensaje de inicio.
        El texto de puntuación se crea aquí para reflejar siempre el valor
        actualizado de ``window.high_score``.
        """
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
        """Gestiona la pulsación de cualquier tecla para iniciar el juego.

        Instancia y configura ``GameView``, y la establece como vista activa.
        La importación se realiza aquí de forma local para evitar
        dependencias circulares entre módulos.

        Args:
            symbol (int): Código de la tecla pulsada (constante de Arcade).
            modifiers (int): Máscara de bits con los modificadores activos
                (Shift, Ctrl, Alt, etc.).
        """
        from Scenes.MainGameView import GameView
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)
