from component import Component


class SpriteRenderer(Component):
    # Sprite: an instance of arcade.Sprite
    def __init__(self, sprite):
        super().__init__("SpriteRenderer")
        self.__sprite = sprite

    # Add the "parent" attribute to the sprite (useful later)
    def on_added_to_entity(self):
        self.__sprite.parent = self.parent

    @property
    def sprite(self):
        return self.__sprite

