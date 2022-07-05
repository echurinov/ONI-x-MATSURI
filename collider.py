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
        # Components attached to the parent, cached here for ease of use
        self.transform = None
        self.sprite_renderer = None

        self.__height = None  # Height of the polygon, cached for performance

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
        if self.transform is None:
            self.transform = self.parent.get_component_by_name("Transform")
        new_polygon = []
        for index, point in enumerate(self.__base_polygon):
            new_polygon.append((point[0] + self.transform.position[0],
                                point[1] + self.transform.position[1]))
        self.__polygon = new_polygon
        return self.__polygon

    @property
    def height(self):
        if self.__height is None:
            self.__height = self.__get_polygon_height()
        return self.__height

    def __get_polygon_height(self):
        height = 0
        top = float("-inf")
        bottom = float("inf")
        for point in self.polygon:
            if point[1] > top:
                top = point[1]
            if point[1] < bottom:
                bottom = point[1]
        height = top - bottom
        return height

    # Generates a rectangular hitbox from the sprite
    def generate_hitbox_from_sprite(self):
        if self.sprite_renderer is None:
            self.sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        self.__base_polygon = (
            (self.sprite_renderer.sprite.width / 2, self.sprite_renderer.sprite.height / 2),
            (-self.sprite_renderer.sprite.width / 2, self.sprite_renderer.sprite.height / 2),
            (-self.sprite_renderer.sprite.width / 2, -self.sprite_renderer.sprite.height / 2),
            (self.sprite_renderer.sprite.width / 2, -self.sprite_renderer.sprite.height / 2),
        )
        self.__height = None

    # Generates a "simple" polygon from the sprite
    def generate_simple_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_simple(sprite.texture.image)
        self.__height = None

    # Generates a "detailed" polygon from the sprite
    def generate_polygon_from_sprite(self):
        sprite = self.parent.get_component_by_name("SpriteRenderer").sprite
        self.__base_polygon = arcade.calculate_hit_box_points_detailed(sprite.texture.image)
        self.__height = None
