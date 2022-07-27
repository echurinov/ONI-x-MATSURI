import random

import arcade
import os
import sys

# From arcade online docs
from eventManager import EventManager
from gameManager import GameManager
from screenView import GameView
from screenView import StartView


class GameWindow(arcade.Window):
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        GameManager.gui_camera.resize(width, height)
        GameManager.main_camera.resize(width, height)
        EventManager.trigger_event("Resize", width, height)


def main():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    SCREEN_TITLE = "ONI x MATSURI"
    GameManager.set_paused(True)
    # window = GameView(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    window = GameWindow(500, 500, SCREEN_TITLE, resizable=True, fullscreen=True)
    start_view = StartView()
    window.show_view(start_view)
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
