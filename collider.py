import arcade

from component import Component
from eventManager import EventManager


# Component for handling hitboxes for an entity
# Doesn't do much right now, the actual movement mechanics use
# the arcade check_for_collision function right now
class Collider(Component):

    # Translates a polygon
    @staticmethod
    def translate_polygon(polygon, amount):
        new_polygon = []
        for index, point in enumerate(polygon):
            new_polygon.append((point[0] + amount[0],
                                point[1] + amount[1]))
        return new_polygon

    def __init__(self, auto_generate_polygon="simple"):
        super().__init__("Collider")
        self.__polygon = None  # The polygon that represents the hitbox, lines up with the sprite
        self.__base_polygon = None  # The base polygon that represents the hitbox, not transformed/rotated
        self.__auto_generate_polygon = auto_generate_polygon

    # Generate the polygon when the component is added to an entity
    def on_added_to_entity(self):
        if self.__auto_generate_polygon == "box":
            self.generate_hitbox_from_sprite()
        elif self.__auto_generate_polygon == "simple":
            self.generate_simple_polygon_from_sprite()
        elif self.__auto_generate_polygon == "detailed":
            self.generate_polygon_from_sprite()

    # Gets the actual position of the polygon for an entity (takes into account transforms)
    @property
    def polygon(self):
        new_polygon = []
        transform_comp = self.parent.get_component_by_name("Transform")
        for index, point in enumerate(self.__base_polygon):
            new_polygon.append((point[0] + transform_comp.position[0],
                                point[1] + transform_comp.position[1]))
        self.__polygon = new_polygon
        return self.__polygon

    # Generates a rectangular hitbox from the sprite
    def generate_hitbox_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = (
            (sprite.texture.image.width / 2, sprite.texture.image.height / 2),
            (-sprite.texture.image.width / 2, sprite.texture.image.height / 2),
            (-sprite.texture.image.width / 2, -sprite.texture.image.height / 2),
            (sprite.texture.image.width / 2, -sprite.texture.image.height / 2),
        )

    # Generates a "simple" polygon from the sprite
    def generate_simple_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_simple(sprite.texture.image)

    # Generates a "detailed" polygon from the sprite
    def generate_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_detailed(sprite.texture.image)
