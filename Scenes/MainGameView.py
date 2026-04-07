"""
Módulo que contiene la vista principal del juego.
"""
import random
from constants import *
from Sprites import *

class GameView(arcade.View):
    """Vista principal donde transcurre la partida.

    Gestiona el bucle de juego completo: renderizado del fondo, jugador
    y enemigos; movimiento por teclado; spawn periódico de enemigos;
    detección de colisiones y transición a la pantalla de Game Over.

    Attributes:
        time_elapsed (float): Segundos transcurridos desde el inicio de la partida.
        score_points (int): Puntuación actual calculada en función del tiempo.
        start_x (float): Coordenada X central de la ventana, usada para centrar textos.
        text_main_title (arcade.Text): Texto con el título del juego en pantalla.
        tiempo_spawn (float): Acumulador de tiempo para controlar el intervalo de spawn.
        collision (bool): Indica si el jugador está actualmente en colisión.
        collides_with_sprite (arcade.Sprite | None): Sprite enemigo con el que colisionó
            el jugador, o ``None`` si no hay colisión activa.
        player_list (arcade.SpriteList): Lista que contiene únicamente al jugador.
        sprite_list (arcade.SpriteList): Lista con todos los enemigos activos.
        background_sprite_list (arcade.SpriteList): Lista con el sprite de fondo.
        backgroung_img (arcade.Sprite): Sprite de la imagen de fondo.
        player (Player): Instancia del jugador.
        player_x (float): Posición X lógica del jugador (usada para moverlo suavemente).
        player_y (float): Posición Y lógica del jugador.
        player_directions (dict[str, bool]): Estado de las teclas de movimiento
            (``'left'``, ``'right'``, ``'up'``, ``'down'``).
        player_speed (float): Velocidad de movimiento del jugador en píxeles/segundo.
        enemy_textures (list[dict]): Lista de diccionarios con los datos de cada tipo
            de enemigo: nombre, texturas cargadas y escala aleatoria.
    """
    def __init__(self):
        """Inicializa la vista de juego y precarga todos los recursos visuales.

        Configura el estado inicial de la partida, crea los textos de HUD,
        instancia al jugador y carga las hojas de sprites de todos los tipos
        de enemigos para su uso posterior en el spawn.
        """
        super().__init__()
        self.time_elapsed = 0
        self.score_points = 0

        # Texto en la pantalla
        self.start_x = WINDOW_WIDTH/2

        self.text_main_title = arcade.Text(
            text="Turtle Survival",
            x = self.start_x, y = WINDOW_HEIGHT - DEFAULT_LINE_HEIGHT ,
            color=arcade.color.BLACK,
            font_size=DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel Square",
            anchor_x="center",
            anchor_y="baseline",
        )

        # Para el spawn de enemigos
        self.tiempo_spawn = 0

        # Para las colisiones
        self.collision = False
        self.collides_with_sprite: arcade.Sprite | None = None

        # Generamos la lista para generar varios sprites al mismo tiempo
        # Una para el jugador, otra para los enemigos y otra para el fondo de pantalla
        self.player_list = arcade.SpriteList()
        self.sprite_list = arcade.SpriteList()
        self.background_sprite_list = arcade.SpriteList()

        # Background
        background = "assets/images/background/background1/orig_big.png"
        self.backgroung_img = arcade.Sprite(background, scale=0.6, center_x=WINDOW_WIDTH/2, center_y=WINDOW_HEIGHT/2)
        self.background_sprite_list.append(self.backgroung_img)

        # Texturas para el jugador
        player_sheet = arcade.load_spritesheet("assets/images/sprites/Turtle/Idle.png")
        texture_list = player_sheet.get_texture_grid(size=(48, 48), columns=4, count=4)

        # Texturas para el jugador cuando muera
        player_sheet_death = arcade.load_spritesheet("assets/images/sprites/Turtle/Death.png")
        texture_list_death = player_sheet_death.get_texture_grid(size=(48, 48), columns=6, count=6)

        # Inicializamos el jugador
        self.player = Player(texture_list, texture_list_death)
        self.player.scale = 1.5
        self.player_x = WINDOW_WIDTH/2
        self.player_y = WINDOW_HEIGHT/2
        self.player.position = (self.player_x, self.player_y)
        self.player_list.append(self.player)

        # Añadimos las direcciones que puede ir y su velocidad predeterminada
        self.player_directions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.player_speed = PLAYER_MOVEMENT_SPEED

        # Para los enemigos
        # Cargamos las texturas de los enemigos para usarlas al hacer el spawn
        snake_sheet = arcade.load_spritesheet("assets/images/sprites/Snake/Walk.png")
        octopus_sheet = arcade.load_spritesheet("assets/images/sprites/Octopus/Idle.png")
        shark_sheet = arcade.load_spritesheet("assets/images/sprites/Shark/Idle.png")
        jelly_sheet = arcade.load_spritesheet("assets/images/sprites/Jellyfish/Walk.png")
        angler_sheet = arcade.load_spritesheet("assets/images/sprites/Anglerfish/Walk.png")

        # Guardamos las texturas en una lista para elegir aleatoriamente
        self.enemy_textures = [
            {"name": "snake",
            "textures": snake_sheet.get_texture_grid(size=(48, 48), columns=4, count=4),
             "scale": (random.randint(1,2) + random.random())},
            {"name": "octopus",
             "textures": octopus_sheet.get_texture_grid(size=(48, 48), columns=4, count=4),
             "scale": (random.randint(1,2) + random.random())},
            {"name": "shark",
            "textures": shark_sheet.get_texture_grid(size=(48, 48), columns=4, count=4),
             "scale": (random.randint(1,2) + random.random())},
            {"name": "jelly",
             "textures": jelly_sheet.get_texture_grid(size=(48, 48), columns=4, count=4),
             "scale": (random.randint(1,2) + random.random())},
            {"name": "angler",
             "textures": angler_sheet.get_texture_grid(size=(48, 48), columns=4, count=4),
             "scale":(random.randint(1,2) + random.random())},
        ]

    def setup(self):
        """Prepara el estado inicial de la partida.

        Actualmente preserva la puntuación existente. Ampliar este metodo
        para reiniciar variables de estado si se añade la opción de
        reintentar la partida sin destruir la vista.
        """
        self.score_points = self.score_points

    def add_enemy(self):
        """Genera un enemigo aleatorio en uno de los cuatro bordes de la pantalla.

        Selecciona aleatoriamente el tipo de enemigo y el lado de aparición.
        La dirección y orientación del sprite se ajustan según el lado elegido:
        la serpiente rota 90° al aparecer por arriba o abajo, y el resto de
        enemigos invierten su escala horizontal al aparecer por la derecha.
        """
        enemy_data = random.choice(self.enemy_textures)

        enemy = Player(enemy_data["textures"])
        enemy.scale = enemy_data["scale"]

        side_spawn = [
            {"lado": "up", "x": random.randint(50, WINDOW_WIDTH - 50), "y": WINDOW_HEIGHT + 50,
                    "speed_X": 0, "speed_Y": -MOB_MOVEMENT_SPEED},  # Lado de arriba
            {"lado": "down", "x": random.randint(50, WINDOW_WIDTH - 50), "y": -50,
                    "speed_X": 0, "speed_Y": MOB_MOVEMENT_SPEED},  # Lado abajo
            {"lado": "left", "x": -50 , "y": random.randint(50, WINDOW_HEIGHT - 50),
                    "speed_X": MOB_MOVEMENT_SPEED, "speed_Y": 0}, # Lado izquierdo
            {"lado": "right", "x": WINDOW_WIDTH + 50, "y": random.randint(50, WINDOW_HEIGHT - 50),
                    "speed_X": -MOB_MOVEMENT_SPEED, "speed_Y": 0}, # Lado derecho
        ]

        random_side = random.choice(side_spawn)

        enemy.center_x = random_side["x"]
        enemy.center_y = random_side["y"]
        enemy.lado = random_side["lado"]
        enemy.speed_X = random_side["speed_X"]
        enemy.speed_Y = random_side["speed_Y"]

        if random_side["lado"] == "up":
            if enemy_data["name"] == "snake":
                enemy.angle = 90

        elif random_side["lado"] == "down":
            if enemy_data["name"] == "snake":
                enemy.angle = -90
        elif random_side["lado"] == "left":
            enemy.scale_x = enemy_data["scale"]
        elif random_side["lado"] == "right":
            enemy.scale_x = -enemy_data["scale"]

        self.sprite_list.append(enemy)

    def on_draw(self):
        """Renderiza todos los elementos visuales del frame actual.

        Orden de pintado: fondo → enemigos → jugador → HUD (título y puntos).
        El texto de puntuación se instancia aquí para mostrar siempre el valor
        más reciente de ``score_points``.
        """
        self.clear()

        self.background_sprite_list.draw()
        self.sprite_list.draw()
        self.player_list.draw()

        self.text_main_title.draw()

        text_points = arcade.Text(
            text=f"Points: {self.score_points}",
            x = self.start_x, y = WINDOW_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
            color = arcade.color.BLACK,
            font_size = DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )

        text_points.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Registra la tecla pulsada activando la dirección correspondiente.

        Controles: W → arriba, S → abajo, A → izquierda, D → derecha.

        Args:
            key (int): Código de la tecla pulsada.
            modifiers (int): Máscara de bits con modificadores activos (Shift, Ctrl…).
        """
        if key == arcade.key.W:
            self.player_directions['up'] = True
        if key == arcade.key.S:
            self.player_directions['down'] = True

        if key == arcade.key.A:
            self.player_directions['left'] = True
        if key == arcade.key.D:
            self.player_directions['right'] = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Registra la tecla liberada desactivando la dirección correspondiente.

        Args:
            key (int): Código de la tecla liberada.
            modifiers (int): Máscara de bits con modificadores activos.
        """
        if key == arcade.key.W:
            self.player_directions['up'] = False
        if key == arcade.key.S:
            self.player_directions['down'] = False

        if key == arcade.key.A:
            self.player_directions['left'] = False
        if key == arcade.key.D:
            self.player_directions['right'] = False

    def on_update(self, delta_time: float = 1 / 60, *args, **kwargs):
        """Actualiza la lógica del juego en cada tick.

        Responsabilidades por orden:
        1. Avanza las animaciones de enemigos y jugador.
        2. Incrementa el tiempo y recalcula la puntuación.
        3. Mueve al jugador según las teclas activas y voltea su sprite.
        4. Desplaza cada enemigo hacia el lado opuesto y lo elimina al salir.
        5. Genera un nuevo enemigo cada ``SPAWN_INTERVAL`` segundos.
        6. Detecta colisión jugador-enemigo y activa la animación de muerte.
        7. Transiciona a ``GameOverView`` cuando la animación de muerte termina.

        Args:
            delta_time (float): Tiempo en segundos desde el último frame (default 1/60).
        """

        self.sprite_list.update(delta_time)
        self.player_list.update(delta_time)

        self.time_elapsed += delta_time
        self.score_points = int(self.time_elapsed * POINTS_PER_SECOND)
        self.score_points += int(self.time_elapsed * delta_time)

        # Movimiento del jugador
        if self.player_directions['left']:
            self.player_x -=  self.player_speed * delta_time
            self.player.scale_x = -1.5
        if self.player_directions['right']:
            self.player_x +=  self.player_speed * delta_time
            self.player.scale_x = 1.5
        if self.player_directions['up']:
            self.player_y +=  self.player_speed * delta_time
        if self.player_directions['down']:
            self.player_y -=  self.player_speed * delta_time

        self.player.position = self.player_x, self.player_y

        # Movimiento de enemigos hacia el lado opuesto a la pantalla
        # y eliminación de la lista de sprites
        for mob in self.sprite_list:
            if mob.lado == "up":
                mob.center_y += mob.speed_Y * delta_time

                if mob.center_y < 0:
                    mob.remove_from_sprite_lists()

            if mob.lado == "down":
                mob.center_y += mob.speed_Y * delta_time

                if mob.center_y > WINDOW_HEIGHT + 50:
                    mob.remove_from_sprite_lists()

            if mob.lado == "left":
                mob.center_x += mob.speed_X * delta_time

                if mob.center_x > WINDOW_WIDTH + 50:
                    mob.remove_from_sprite_lists()

            if mob.lado == "right":
                mob.center_x += mob.speed_X * delta_time

                if mob.center_x < 0:
                    mob.remove_from_sprite_lists()

        # Spawn periódico de enemigos
        self.tiempo_spawn += delta_time
        if self.tiempo_spawn >= SPAWN_INTERVAL:
            self.add_enemy()
            self.tiempo_spawn = 0

        # Detección de colisión y muerte del jugador
        hit = arcade.check_for_collision_with_list(self.player, self.sprite_list)

        if hit:
            self.collides_with_sprite = hit[0]
            self.player.die()
            self.player_speed = 0

        else:
            if self.collides_with_sprite:
                self.collides_with_sprite = None
            self.collision = False

        # Transición a pantalla de game over si ha muerto
        if self.player.ready_for_game_over:
            from Scenes.GameOverView import GameOverView
            game_over_view = GameOverView(self.score_points)
            self.window.show_view(game_over_view)
