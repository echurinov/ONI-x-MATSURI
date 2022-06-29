from component import Component


class SpriteRenderer(Component):
    # Sprite: an instance of arcade.Sprite
    def __init__(self, sprite):
        super().__init__("SpriteRenderer")
        self.__sprite = sprite


    @property
    def sprite(self):
        return self.__sprite

