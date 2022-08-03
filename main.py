import sys
import os
os.chdir(os.path.dirname(sys.modules['__main__'].__file__))
import random
import arcade

# From arcade online docs
from eventManager import EventManager
from gameManager import GameManager
from musicManager import MusicManager
from screenView import GameView
from screenView import StartView
from soundManager import SoundManager


class GameWindow(arcade.Window):
    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)
        #GameManager.gui_camera.resize(width, height)
        EventManager.trigger_event("Resize", width, height)


def main():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        os.chdir(sys._MEIPASS)
    SCREEN_TITLE = "ONI x MATSURI"
    GameManager.set_paused(True)
    # window = GameView(GameManager.SCREEN_WIDTH, GameManager.SCREEN_HEIGHT, SCREEN_TITLE)
    window = GameWindow(1000, 700, SCREEN_TITLE, resizable=True, fullscreen=True)
    SoundManager.start()
    MusicManager.start()
    start_view = StartView()
    MusicManager.change_list("start_view")
    MusicManager.play_song()
    window.show_view(start_view)
    GameManager.start()
    window.run()


if __name__ == '__main__':
    main()
