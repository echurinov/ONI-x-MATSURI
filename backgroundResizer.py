from component import Component
from gameManager import GameManager

# Resizes the background to fit the window
class BackgroundResizer(Component):
    def __init__(self):
        super().__init__("BackgroundResizer")
        self.__sprite = None

    def on_added_to_entity(self):
        pass

    def on_update(self, dt):
        return
        GameManager.SCREEN_HEIGHT