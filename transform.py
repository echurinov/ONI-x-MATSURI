import arcade

from component import Component


# Component for handling position, rotation, and scale of an Entity
from gameManager import GameManager


class Transform(Component):
    def __init__(self, position=(0, 0), rotation=0, scale=1.0):
        super().__init__("Transform")
        self.__position = position
        self.__rotation = rotation
        self.__scale = scale

    # Called when the Entity is created
    def on_created(self):
        sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        if sprite_renderer is not None:
            sprite_renderer.sprite.center_x = self.position[0]
            sprite_renderer.sprite.center_y = self.position[1]
            sprite_renderer.sprite.scale = self.__scale

    @property
    def scale(self):
        return self.__scale

    @scale.setter
    def scale(self, value):
        self.__scale = value
        sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        if sprite_renderer is not None:
            sprite_renderer.sprite._scale = self.__scale
        collider = self.parent.get_component_by_name("Collider")
        if collider is not None:
            collider.set_scale(self.__scale)


    @property
    def rotation(self):
        return self.__rotation

    # Sets the rotation of the Entity
    @rotation.setter
    def rotation(self, value):
        self.__rotation = value
        sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        if sprite_renderer is not None:
            sprite_renderer.sprite.angle = value  # Changes the rotation of arcade Sprite

    @property
    def position(self):
        return self.__position

    # Sets the position of the Entity
    @position.setter
    def position(self, value):
        if len(value) == 2:
            self.__position = value
            sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
            if sprite_renderer is not None:
                # Changes the position of arcade Sprite
                sprite_renderer.sprite.center_x = value[0]
                sprite_renderer.sprite.center_y = value[1]
        else:
            raise ValueError("Position must be a tuple of length 2 (Got tuple of length " + str(len(value)) + ").")

    # Move an Entity by a certain amount
    def move(self, amount):
        if len(amount) == 2:
            self.position = (self.position[0] + amount[0], self.position[1] + amount[1])
        else:
            raise ValueError("Amount must be a tuple of length 2 (Got tuple of length " + str(len(amount)) + ").")

