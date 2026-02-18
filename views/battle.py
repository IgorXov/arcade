import arcade
from config import *
from entities.projectile import Projectile


class BattleView(arcade.View):

    def __init__(self):
        super().__init__()

        self.box_center_x = SCREEN_WIDTH // 2
        self.box_center_y = SCREEN_HEIGHT // 2

        self.box_left = self.box_center_x - BATTLE_BOX_WIDTH // 2
        self.box_right = self.box_center_x + BATTLE_BOX_WIDTH // 2
        self.box_bottom = self.box_center_y - BATTLE_BOX_HEIGHT // 2
        self.box_top = self.box_center_y + BATTLE_BOX_HEIGHT // 2

        self.soul = arcade.Sprite("assets/soul.png", scale=1)
        self.soul.center_x = self.box_center_x
        self.soul.center_y = self.box_center_y

        self.soul_list = arcade.SpriteList()
        self.soul_list.append(self.soul)

        self.projectiles = arcade.SpriteList()

        self.spawn_timer = 0.0
        self.spawn_interval = 1.0
        self.hp = 20

        self.soul_speed = 25  # пикселей в секунду

        arcade.set_background_color(arcade.color.BLACK)


    def on_draw(self):
        self.clear()



        self.soul_list.draw()
        self.projectiles.draw()

        arcade.draw_text(
            f"HP: {self.hp}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

    def on_update(self, delta_time: float):

        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_projectile()
            self.spawn_timer = 0.0

        self.soul_list.update(delta_time)
        self.projectiles.update(delta_time)

        self.soul.center_x = max(self.box_left, min(self.box_right, self.soul.center_x))
        self.soul.center_y = max(self.box_bottom, min(self.box_top, self.soul.center_y))

        hit_list = arcade.check_for_collision_with_list(
            self.soul, self.projectiles
        )

        for projectile in hit_list:
            projectile.remove_from_sprite_lists()
            self.hp -= 1

        if self.hp <= 0:
            from views.overworld import OverworldView
            self.window.show_view(OverworldView())


    def spawn_projectile(self):
        projectile = Projectile(
            self.box_center_x,
            self.box_top
        )
        self.projectiles.append(projectile)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.soul.change_y = self.soul_speed
        elif key == arcade.key.S:
            self.soul.change_y = -self.soul_speed
        elif key == arcade.key.A:
            self.soul.change_x = -self.soul_speed
        elif key == arcade.key.D:
            self.soul.change_x = self.soul_speed
        elif key == arcade.key.ESCAPE:
            from views.overworld import OverworldView
            self.window.show_view(OverworldView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.soul.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.soul.change_x = 0
