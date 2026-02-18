import arcade
from entities.player import Player
from views.battle import BattleView
from config import *


class OverworldView(arcade.View):

    def __init__(self):
        super().__init__()

        self.player = Player()
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        # ВАЖНО: создаём SpriteList
        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

    def on_draw(self):
        self.clear()

        # Теперь рисуем список
        self.player_list.draw()

        arcade.draw_text(
            "Press SPACE to start battle",
            10,
            10,
            arcade.color.WHITE,
            14,
        )

    def on_update(self, delta_time):
        self.player_list.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.player.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.player.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.player.speed
        elif key == arcade.key.D:
            self.player.change_x = self.player.speed
        elif key == arcade.key.SPACE:
            self.window.show_view(BattleView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0
