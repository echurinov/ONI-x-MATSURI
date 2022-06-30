import arcade

from component import Component
from eventManager import EventManager


class Collider(Component):
    def __init__(self, auto_generate_polygon="simple"):
        super().__init__("Collider")
        self.__polygon = None
        self.__base_polygon = None
        self.__auto_generate_polygon = auto_generate_polygon

    def on_added_to_entity(self):
        if self.__auto_generate_polygon == "box":
            self.generate_hitbox_from_sprite()
        elif self.__auto_generate_polygon == "simple":
            self.generate_simple_polygon_from_sprite()
        elif self.__auto_generate_polygon == "detailed":
            self.generate_polygon_from_sprite()

    @property
    def polygon(self):
        new_polygon = []
        transform_comp = self.parent.get_component_by_name("Transform")
        for index, point in enumerate(self.__base_polygon):
            new_polygon.append((point[0] + transform_comp.position[0],
                                point[1] + transform_comp.position[1]))
        self.__polygon = new_polygon
        return self.__polygon

    def generate_hitbox_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = (
            (sprite.texture.image.width / 2, sprite.texture.image.height / 2),
            (-sprite.texture.image.width / 2, sprite.texture.image.height / 2),
            (-sprite.texture.image.width / 2, -sprite.texture.image.height / 2),
            (sprite.texture.image.width / 2, -sprite.texture.image.height / 2),
        )

    def generate_simple_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_simple(sprite.texture.image)

    def generate_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_detailed(sprite.texture.image)
