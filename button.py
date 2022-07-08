import arcade

import arcade.gui
from screenView import GameView


class StartButton(arcade.gui.UITextureButton):
    def __init__(self, current_view: arcade.View, *args):
        super().__init__(*args)
        self.View = current_view

    def on_click_button(self, event):
        game_view = GameView()
        game_view.setup()
        self.View.window.show_view(game_view)


class QuitButton(arcade.gui.UITextureButton):
    def __init__(self, *args):
        super().__init__(*args)

    def on_click_button(self, event):
        arcade.quit()
