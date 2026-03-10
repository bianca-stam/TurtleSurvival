import random

import arcade
from arcade.clock import GLOBAL_CLOCK

# ---------
# CONSTANES
# ---------

# Para la ventana
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 720
WINDOW_TITLE = "FishyFishy"

# Para el texto
DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 20
arcade.resources.load_kenney_fonts()
arcade.resources.load_liberation_fonts()

# Para el movimiento
PLAYER_MOVEMENT_SPEED = 200
MOB_MOVEMENT_SPEED = 300
SPAWN_INTERVAL = 0.5  # segundos entre cada enemigo

window = arcade.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
window.center_window()
window.background_color = arcade.color.BABY_BLUE


# Clase para controlar el jugador que hereda la de la classe arcade.Sprite
class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture]):
        super().__init__(texture_list[0])
        self.textures = texture_list

        self.time_elapsed = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.time_elapsed += delta_time

        # Configuramos las texturas
        if self.time_elapsed > 0.35:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)  # set_texture viene de la clase de arcade.Sprite
                self.cur_texture_index += 1
            self.time_elapsed = 0

        if self.cur_texture_index == 3:
            self.cur_texture_index = 0


class GameView(arcade.View):
    """
    Main application class.
    """
    def __init__(self):
        super().__init__()

        self.score_points = 0
        self.time_elapsed = 0

        # Add the screen title
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
        self.hit_base_color = arcade.color.WHITE
        self.hit_coll_color = arcade.color.RED
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

        # Para el jugador
        player_sheet = arcade.load_spritesheet("assets/images/sprites/Turtle/Idle.png")
        texture_list = player_sheet.get_texture_grid(size=(48, 48), columns=4, count=4)

        self.player = Player(texture_list)
        self.player.scale = 1.5
        self.player_x = WINDOW_WIDTH/2
        self.player_y = WINDOW_HEIGHT/2
        self.player.position = (self.player_x, self.player_y)
        self.player_list.append(self.player)

        self.player_directions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.player_speed = PLAYER_MOVEMENT_SPEED

        # Para los enemigos
        # Cargamos las texturas de los enemigos para usarlas al hacer spawn
        snake_sheet = arcade.load_spritesheet("assets/images/sprites/Snake/Walk.png")
        octopus_sheet = arcade.load_spritesheet("assets/images/sprites/Octopus/Idle.png")
        shark_sheet = arcade.load_spritesheet("assets/images/sprites/Shark/Idle.png")
        jelly_sheet = arcade.load_spritesheet("assets/images/sprites/Jellyfish/Walk.png")
        angler_sheet = arcade.load_spritesheet("assets/images/sprites/Anglerfish/Walk.png")

        # Guardamos las texturas en una lista para elegir aleatoriamente
        self.enemy_textures = [
            {"textures": snake_sheet.get_texture_grid(size=(48, 48), columns=4, count=4), "scale": random.randint(1, 3)},
            {"textures": octopus_sheet.get_texture_grid(size=(48, 48), columns=4, count=4), "scale": random.randint(1, 3)},
            {"textures": shark_sheet.get_texture_grid(size=(48, 48), columns=4, count=4), "scale": random.randint(1, 3)},
            {"textures": jelly_sheet.get_texture_grid(size=(48, 48), columns=4, count=4), "scale": random.randint(1, 3)},
            {"textures": angler_sheet.get_texture_grid(size=(48, 48), columns=4, count=4), "scale": random.randint(1, 3)},
        ]


    def add_enemy(self):
        """Crea un enemigo aleatorio en el borde izquierdo de la pantalla"""
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

        self.sprite_list.append(enemy)

    def setup(self):
        pass

    def reset(self):
        self.start_time = GLOBAL_CLOCK.time

    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw()
        self.sprite_list.draw()
        self.player_list.draw()

        if self.collision:
            self.player_list.draw_hit_boxes(self.hit_coll_color)
        else:
            self.player_list.draw_hit_boxes(self.hit_base_color)

        self.sprite_list.draw_hit_boxes(self.hit_base_color)

        self.text_main_title.draw()

        self.text_points = arcade.Text(
            text=f"Points: {self.score_points}",
            x = self.start_x, y = WINDOW_HEIGHT - DEFAULT_LINE_HEIGHT * 1.5,
            color = arcade.color.BLACK,
            font_size = DEFAULT_FONT_SIZE,
            font_name="Kenney Pixel",
            anchor_x="center",
            anchor_y="baseline",
        )
        self.text_points.draw()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called whenever a key is pressed. """
        if key == arcade.key.W:
            self.player_directions['up'] = True
        if key == arcade.key.S:
            self.player_directions['down'] = True

        if key == arcade.key.A:
            self.player_directions['left'] = True
        if key == arcade.key.D:
            self.player_directions['right'] = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key. """
        if key == arcade.key.W:
            self.player_directions['up'] = False
        if key == arcade.key.S:
            self.player_directions['down'] = False

        if key == arcade.key.A:
            self.player_directions['left'] = False
        if key == arcade.key.D:
            self.player_directions['right'] = False

    def on_update(self, delta_time: float) -> None:
        self.sprite_list.update()
        self.player_list.update()

        self.time_elapsed += delta_time
        self.score_points = int(self.time_elapsed * 1)  # 1 punto por segundo
        self.score_points += int(self.time_elapsed * delta_time)

        if self.player_directions['left']:
            self.player_x -=  self.player_speed * delta_time
        if self.player_directions['right']:
            self.player_x +=  self.player_speed * delta_time
        if self.player_directions['up']:
            self.player_y +=  self.player_speed * delta_time
        if self.player_directions['down']:
            self.player_y -=  self.player_speed * delta_time

        self.player.position = self.player_x, self.player_y

        # Mover enemigos hacia el lado opuesto a la pantalla e eliminarlos de la lista
        for enemy in self.sprite_list:
            if enemy.lado == "up":
                enemy.center_y += enemy.speed_Y * delta_time

                if enemy.center_y < 0:
                    enemy.remove_from_sprite_lists()

            if enemy.lado == "down":
                enemy.center_y += enemy.speed_Y * delta_time

                if enemy.center_y > WINDOW_HEIGHT + 50:
                    enemy.remove_from_sprite_lists()

            if enemy.lado == "left":
                enemy.center_x += enemy.speed_X * delta_time

                if enemy.center_x > WINDOW_WIDTH + 50:
                    enemy.remove_from_sprite_lists()

            if enemy.lado == "right":
                enemy.center_x += enemy.speed_X * delta_time

                if enemy.center_x < 0:
                    enemy.remove_from_sprite_lists()

        # Spawn de enemigos cada SPAWN_INTERVAL segundos
        self.tiempo_spawn += delta_time
        if self.tiempo_spawn >= SPAWN_INTERVAL:
            self.add_enemy()
            self.tiempo_spawn = 0

        hit =  arcade.check_for_collision_with_list(self.player, self.sprite_list)

        if hit:
            self.collides_with_sprite = hit[0]
            self.collides_with_sprite_color = self.hit_coll_color
            self.collision = True
        else:
            if self.collides_with_sprite:
                self.collides_with_sprite.color = self.hit_base_color
                self.collides_with_sprite = None
            self.collision = False


game = GameView()
window.show_view(game)
arcade.run()
