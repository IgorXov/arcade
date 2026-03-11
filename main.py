import arcade
from config import *
from views.overworld import OverworldView


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.show_view(OverworldView())
    arcade.run()


if __name__ == "__main__":
    main()
