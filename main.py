import arcade

# Constants
# Para la ventana
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "FishyFishy"

# Para el movimiento
MOVEMENT_SPEED = 500

window = arcade.Window(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, title=WINDOW_TITLE)
window.center_window()
window.background_color = arcade.color.BABY_BLUE


# Clase para controlar el jugador que hereda la de arcade.Sprite
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

        # Generamos la lista para generar varios sprites al mismo tiempo
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
        self.player.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.player_list.append(self.player)

        self.directions = {'left': False, 'right': False, 'up': False, 'down': False}
        self.player_x = 640
        self.player_y = 360
        self.player_speed = MOVEMENT_SPEED

        # Para los enemigos
        # La medusita
        jelly_sheet = arcade.load_spritesheet("assets/images/sprites/Jellyfish/Walk.png")
        jelly_texture_list = jelly_sheet.get_texture_grid(size=(48, 48), columns=4, count=4)

        self.jellyfish = Player(jelly_texture_list)
        self.jellyfish.scale = 1.5
        self.jellyfish.position = (WINDOW_WIDTH / 3, WINDOW_HEIGHT / 3)
        self.sprite_list.append(self.jellyfish)
        # La serpiente
        snake_sheet = arcade.load_spritesheet("assets/images/sprites/Snake/Walk.png")
        snake_texture_list = snake_sheet.get_texture_grid(size=(48, 48), columns=4, count=4)

        self.snake = Player(snake_texture_list)
        self.snake.scale = 1.5
        self.snake.position = (100, 100)
        self.sprite_list.append(self.snake)

        # Para las colisiones
        self.hit_base_color = arcade.color.WHITE
        self.hit_coll_color = arcade.color.RED
        self.collision = False

        self.collides_with_sprite: arcade.Sprite | None = None

        """
        # Añadimos la animación
        frames = []
        for tex in texture_list:
            frames.append(arcade.TextureKeyframe(tex))  # TextureKeyframe Una foto individual

        anim = arcade.TextureAnimation(frames)  # El álbum de fotos ordenado
        self.animPlayer = arcade.TextureAnimationSprite(animation=anim)  # La persona que hojea el álbum
        self.animPlayer.position = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.sprite_list.append(self.animPlayer)
        """

    def setup(self):
        pass

    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw()
        self.sprite_list.draw()
        self.player_list.draw()

        # sarcade.draw_ellipse_filled(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, 30, 30, arcade.color.BALL_BLUE)

        # draw_text es muy lento, sólo para debuggear!
        # arcade.draw_text(f"x = {self.circle_x:.2f}, y = {self.circle_y:.2f}",
        #                 10, 700,
        #                 arcade.color.BLACK, 14)s

        if self.collision:
            self.player_list.draw_hit_boxes(self.hit_coll_color)
        else:
            self.player_list.draw_hit_boxes(self.hit_base_color)

        self.sprite_list.draw_hit_boxes(self.hit_base_color)

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Called whenever a key is pressed. """
        if key == arcade.key.W:
            self.directions['up'] = True
        if key == arcade.key.S:
            self.directions['down'] = True

        if key == arcade.key.A:
            self.directions['left'] = True
        if key == arcade.key.D:
            self.directions['right'] = True

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Called when the user releases a key. """
        if key == arcade.key.W:
            self.directions['up'] = False
        if key == arcade.key.S:
            self.directions['down'] = False

        if key == arcade.key.A:
            self.directions['left'] = False
        if key == arcade.key.D:
            self.directions['right'] = False

    def on_update(self, delta_time: float) -> None:
        self.sprite_list.update()

        if self.directions['left']:
            self.player_x -=  self.player_speed * delta_time
        if self.directions['right']:
            self.player_x +=  self.player_speed * delta_time
        if self.directions['up']:
            self.player_y +=  self.player_speed * delta_time
        if self.directions['down']:
            self.player_y -=  self.player_speed * delta_time

        self.player.position = self.player_x, self.player_y

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
