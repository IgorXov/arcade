import arcade
from config import PLAYER_SPEED


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__("assets/player/PC _ Computer - Undertale - Frisk - Walk Down.gif", scale=2)

        self.speed = PLAYER_SPEED

        self.walk_textures = [
            arcade.load_texture("assets/player/PC _ Computer - Undertale - Frisk - Walk Down.gif"),
            arcade.load_texture("assets/player/PC _ Computer - Undertale - Frisk - Walk Down.gif"),
        ]

        self.idle_texture = arcade.load_texture("assets/player/PC _ Computer - Undertale - Frisk - Walk Down.gif")

        self.animation_timer = 0
        self.current_texture_index = 0

    def update(self, delta_time: float = 1 / 60):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.change_x != 0 or self.change_y != 0:
            self.animation_timer += delta_time
            if self.animation_timer > 0.15:
                self.animation_timer = 0
                self.current_texture_index = (
                                                     self.current_texture_index + 1
                                             ) % len(self.walk_textures)
                self.texture = self.walk_textures[self.current_texture_index]
        else:
            self.texture = self.idle_texture
