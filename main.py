import arcade
from config import *
from views.overworld import OverworldView


class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

def main():
    window = GameWindow()
    view = OverworldView()
    window.show_view(view)
    arcade.run()

if __name__ == '__main__':
    main()
