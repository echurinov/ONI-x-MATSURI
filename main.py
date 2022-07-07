import random

import arcade

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
    SCREEN_TITLE = "ONI x MATSURI"
    GameManager.set_paused(True)
    # window = GameView(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    window = GameWindow(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE, resizable=True, fullscreen=True)
    start_view = StartView()
    window.show_view(start_view)
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
