import arcade
from config import SCREEN_WIDTH, SCREEN_HEIGHT, asset_path


class BattleBaseView(arcade.View):

    def __init__(self):
        super().__init__()

        arcade.set_background_color(arcade.color.BLACK)

        self.soul = arcade.Sprite(asset_path("player", "soul.png"), scale=1)
        self.soul.center_x = SCREEN_WIDTH // 2
        self.soul.center_y = 150

        self.soul_list = arcade.SpriteList()
        self.soul_list.append(self.soul)

        self.info_text = arcade.Text(
            "Battle Mode",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20,
            anchor_x="center"
        )

    def on_draw(self):
        self.clear()

        self.soul_list.draw()
        self.info_text.draw()

    def on_update(self, delta_time):
        self.soul_list.update()