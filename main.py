import random

import arcade

# From arcade online docs
from gameManager import GameManager
from screenView import GameView
from screenView import StartView


def main():
    SCREEN_TITLE = "ONI x MATSURI"

    # window = GameView(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    window = arcade.Window(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = GameView()
    window.show_view(start_view)
    # window.setup()
    start_view.setup()
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
