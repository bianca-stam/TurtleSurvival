"""
Módulo que contiene la clase Player, sprite animado del jugador y los enemigos.
"""

import arcade

class Player(arcade.Sprite):
    """Sprite animado que representa al jugador o a un enemigo.

    Hereda de ``arcade.Sprite`` y añade soporte para dos animaciones:
    idle (bucle continuo) y muerte (secuencia lineal con callback al juego).
    La misma clase se reutiliza para los enemigos, que sólo usan la
    animación idle al no recibir ``death_texture_list``.

    Attributes:
        textures (list[arcade.Texture]): Frames de la animación idle en bucle.
        time_elapsed (float): Acumulador de tiempo para cadenciar los frames.
        death_texture (list[arcade.Texture] | None): Frames de la animación de
            muerte, o ``None`` si el sprite no tiene animación de muerte.
        is_dead (bool): ``True`` desde el momento en que se llama a :meth:`die`.
        death_animation_done (bool): ``True`` cuando se ha mostrado el último
            frame de muerte y la animación ha concluido.
        death_texture_index (int): Índice del frame de muerte actual.
        death_timer (float): Segundos transcurridos tras terminar la animación
            de muerte; controla el retardo antes de pasar a Game Over.
        ready_for_game_over (bool): Flag que la vista de juego consulta para
            saber cuándo debe transicionar a la pantalla de Game Over.
    """
    def __init__(self, texture_list: list[arcade.Texture], death_texture_list: list[arcade.Texture] | None = None):
        """Inicializa el sprite con las texturas de idle y, opcionalmente, de muerte.

        El primer frame de ``texture_list`` se usa como textura inicial del sprite.

        Args:
            texture_list (list[arcade.Texture]): Secuencia de frames para la
                animación idle, reproducida en bucle mientras el sprite esté vivo.
            death_texture_list (list[arcade.Texture] | None): Secuencia de frames
                para la animación de muerte. Si es ``None``, el sprite no tiene
                animación de muerte (comportamiento por defecto en enemigos).
        """
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
        """Activa la secuencia de muerte del sprite.

        Idempotente: si el sprite ya está muerto, la llamada no tiene efecto.
        Reinicia el índice de animación y muestra el primer frame de muerte
        de forma inmediata sin esperar al siguiente tick.
        """
        if not self.is_dead:
            self.is_dead = True
            self.cur_texture_index = 0

            # Muestra el primer frame de muerte inmediatamente
            if self.death_texture:
                self.texture = self.death_texture[0]

    def update(self, delta_time: float = 1 / 60, *args, **kwargs):
        """Avanza la animación del sprite un tick.

        Lógica según el estado del sprite:

        - Vivo: cicla los frames de idle cada 0.35 s en bucle (frames 0-2).
        - Muerto, animando: avanza un frame de muerte cada 0.25 s hasta
          agotar la secuencia; entonces congela el último frame.
        - Muerto, animación terminada: espera 1 s y activa
          ``ready_for_game_over`` para que la vista de juego cambie de escena.

        Args:
            delta_time (float): Tiempo en segundos desde el último frame
                (por defecto 1/60 para 60 FPS).
        """
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
                    self.ready_for_game_over = True  # Avisa al juego para cambiar a game over
            return


        # -- Animación de nadando --
        if self.time_elapsed > 0.35:
            if self.cur_texture_index < len(self.textures):
                self.set_texture(self.cur_texture_index)
                self.cur_texture_index += 1
            self.time_elapsed = 0

        if self.cur_texture_index == 3:
            self.cur_texture_index = 0



