from component import Component
from eventManager import EventManager
from gameManager import GameManager


# Resizes the background to fit the window
class BackgroundResizer(Component):
    def __init__(self, original_height=1080):
        super().__init__("BackgroundResizer")
        self.__sprite = None
        self.__original_position = None
        self.__original_height = original_height
        self.__transform = None

        EventManager.add_listener("Resize", self.on_resize)

    def on_created(self):
        self.__sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__original_position = self.parent.get_component_by_name("Transform").position
        self.__transform = self.parent.get_component_by_name("Transform")

    def on_resize(self, width, height):
        new_scale = height / self.__original_height
        self.__sprite.scale = new_scale
        print(new_scale)
        self.__transform.position = (self.__original_position[0] * new_scale, self.__original_position[1] * new_scale)
