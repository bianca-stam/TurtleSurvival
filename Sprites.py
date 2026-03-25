import arcade

# Clase para controlar el jugador que hereda la de la classe arcade.Sprite
class Player(arcade.Sprite):
    def __init__(self, texture_list: list[arcade.Texture], death_texture_list: list[arcade.Texture] | None = None):
        super().__init__(texture_list[0])
        self.textures = texture_list
        self.time_elapsed = 0

        self.death_texture = death_texture_list
        self.is_dead = False
        self.death_animation_done = False
        self.death_texture_index = 0

        self.death_timer = 0.0  # Contador post-muerte
        self.ready_for_game_over = False  # Flag para avisar al juego

    # Clase para en caso de que el sprite muera
    def die(self):
        if not self.is_dead:
            self.is_dead = True
            self.cur_texture_index = 0

            # Muestra el primer frame de muerte inmediatamente
            if self.death_texture:
                self.texture = self.death_texture[0]

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        self.time_elapsed += delta_time

        # --- Animación de muerte ---
        if self.is_dead:

            if self.death_texture and not self.death_animation_done:
                if self.time_elapsed > 0.25:
                    self.cur_texture_index += 1

                    if self.cur_texture_index >= len(self.death_texture):
                        # Animación terminada, se congela en el último frame
                        self.cur_texture_index = len(self.death_texture) - 1
                        self.death_animation_done = True

                    self.texture = self.death_texture[self.cur_texture_index]
                    self.time_elapsed = 0

            if self.death_animation_done:
                self.death_timer += delta_time
                if self.death_timer >= 1.0:
                    self.ready_for_game_over = True  # 👈 Avisa al juego
            return


        # Configuramos las texturas
        if self.time_elapsed > 0.35:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)  # set_texture viene de la clase de arcade.Sprite
                self.cur_texture_index += 1
            self.time_elapsed = 0

        if self.cur_texture_index == 3:
            self.cur_texture_index = 0



