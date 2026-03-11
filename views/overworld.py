import arcade
import random
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    asset_path,
    lerp_color,
    COLOR_BG_TOP,
    COLOR_BG_BOTTOM,
    COLOR_TEXT,
    COLOR_TEXT_DIM,
    COLOR_ACCENT,
    BACKGROUND_STEPS,
)
from stats import get_stats_lines


class OverworldView(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.DARK_BLUE)

        self.player = arcade.Sprite(asset_path("player", "soul.png"), scale=1)
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list = arcade.SpriteList()
        self.player_list.append(self.player)

        self.speed = 250

        self.stars = []
        for _ in range(80):
            self.stars.append({
                "x": random.uniform(0, SCREEN_WIDTH),
                "y": random.uniform(0, SCREEN_HEIGHT),
                "r": random.uniform(1.0, 2.4),
                "a": random.randint(50, 130),
                "tw": random.uniform(0.3, 1.0),
            })

    def on_draw(self):
        self.clear()
        self.draw_background()

        self.player_list.draw()

        arcade.draw_text(
            "Press SPACE to open Level Menu",
            20,
            SCREEN_HEIGHT - 40,
            COLOR_ACCENT,
            18,
        )

        stats_lines = get_stats_lines()
        y = 20
        for line in stats_lines:
            arcade.draw_text(
                line,
                20,
                y,
                COLOR_TEXT_DIM,
                14,
            )
            y += 18

    def draw_background(self):
        step_h = SCREEN_HEIGHT / BACKGROUND_STEPS
        for i in range(BACKGROUND_STEPS):
            t = i / max(1, BACKGROUND_STEPS - 1)
            color = lerp_color(COLOR_BG_BOTTOM, COLOR_BG_TOP, t)
            arcade.draw_lrbt_rectangle_filled(
                0,
                SCREEN_WIDTH,
                i * step_h,
                (i + 1) * step_h,
                color
            )

        for star in self.stars:
            arcade.draw_circle_filled(
                star["x"],
                star["y"],
                star["r"],
                (255, 255, 255, star["a"])
            )

    def on_update(self, delta_time):
        self.player_list.update()

        for star in self.stars:
            star["a"] += star["tw"] * delta_time * 60
            if star["a"] > 150 or star["a"] < 40:
                star["tw"] *= -1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player.change_y = self.speed
        elif key == arcade.key.S:
            self.player.change_y = -self.speed
        elif key == arcade.key.A:
            self.player.change_x = -self.speed
        elif key == arcade.key.D:
            self.player.change_x = self.speed
        elif key == arcade.key.SPACE:
            from views.level_select import LevelSelectView
            self.window.show_view(LevelSelectView())

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player.change_x = 0
