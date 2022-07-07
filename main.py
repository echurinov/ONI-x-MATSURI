import random

import arcade

from gameManager import GameManager
from screenView import GameView
from screenView import StartView


def main():
    SCREEN_TITLE = "ONI x MATSURI"

    window = arcade.Window(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
