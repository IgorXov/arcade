import arcade


class Projectile(arcade.Sprite):

    def __init__(self, x, y):
        super().__init__("assets/projectile.png", scale=1)
        self.center_x = x
        self.center_y = y
        self.speed = 200

    def update(self, delta_time: float = 1/60):
        self.center_y -= self.speed * delta_time

        if self.center_y < 0:
            self.remove_from_sprite_lists()
