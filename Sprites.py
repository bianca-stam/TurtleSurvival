import arcade

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