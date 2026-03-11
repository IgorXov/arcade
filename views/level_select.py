# views/level_select.py
import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class LevelSelectView(arcade.View):

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.BLACK)

        self.selected = 0
        self.levels = 7

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "CHOOSE LEVEL",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 100,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

        for i in range(self.levels):
            color = arcade.color.YELLOW if i == self.selected else arcade.color.WHITE

            arcade.draw_text(
                f"Level {i + 1}",
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT - 180 - i * 40,
                color,
                20,
                anchor_x="center",
            )

        arcade.draw_text(
            "ENTER - start   ESC - back",
            SCREEN_WIDTH // 2,
            60,
            arcade.color.GRAY,
            16,
            anchor_x="center",
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP:
            self.selected = (self.selected - 1) % self.levels

        elif key == arcade.key.DOWN:
            self.selected = (self.selected + 1) % self.levels

        elif key == arcade.key.ENTER:
            self.start_level()

        elif key == arcade.key.ESCAPE:
            from views.overworld import OverworldView
            self.window.show_view(OverworldView())

    def start_level(self):

        level_number = self.selected + 1

        if level_number == 1:
            from views.level_1 import Level1
            self.window.show_view(Level1())
        elif level_number == 2:
            from views.level_2 import Level2
            self.window.show_view(Level2())
        elif level_number == 3:
            from views.level_3 import Level3
            self.window.show_view(Level3())
        elif level_number == 4:
            from views.level_4 import Level4
            self.window.show_view(Level4())
        elif level_number == 5:
            from views.level_5 import Level5
            self.window.show_view(Level5())
        elif level_number == 6:
            from views.level_6 import Level6
            self.window.show_view(Level6())
        elif level_number == 7:
            from views.level_7 import Level7
            self.window.show_view(Level7())