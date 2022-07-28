import arcade

from collider import Collider
from entity import Entity
from spriteRenderer import SpriteRenderer
from transform import Transform
from eventManager import EventManager
from gameManager import GameManager


BOUNCE_TIME = 0.3
BOUNCE_AMOUNT = 7

class PowerUpHealth(Entity):
    def __init__(self, position):
        self.__floor_sprite = arcade.Sprite("assets/sprites/cottoncandy.png")
        floor_sprite_renderer = SpriteRenderer(self.__floor_sprite)
        floor_transform = Transform(position, 0, (0.25, 0.25))
        floor_collider = Collider(auto_generate_polygon="box")
        super(PowerUpHealth, self).__init__("Block", ["PowerUp"], [floor_sprite_renderer, floor_transform, floor_collider],
                                          static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__collection_timer = 0.3

        self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
            "PlayerController")

        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame


    def on_physics_update(self, dt):
        self.__collection_timer -= dt
        if self.__collection_timer < 0:
            self.__color_done = True
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__floor_sprite.set_position(self.__floor_sprite.position[0], self.__floor_sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        if self.__player_controller.health < self.__player_controller.max_health:
            self.__player_controller.set_health(self.__player_controller.health + 1)

        GameManager.remove_entity(self)
        return "Health-Up"

class PowerUpSpeed(Entity):
    def __init__(self, position):
        self.__floor_sprite = arcade.Sprite("assets/sprites/onigiri.png")
        floor_sprite_renderer = SpriteRenderer(self.__floor_sprite)
        floor_transform = Transform(position, 0, (0.25, 0.25))
        floor_collider = Collider(auto_generate_polygon="box")
        super(PowerUpSpeed, self).__init__("Block", ["PowerUp"], [floor_sprite_renderer, floor_transform, floor_collider],
                                          static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
            "PlayerController")

        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame


    def on_physics_update(self, dt):
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__floor_sprite.set_position(self.__floor_sprite.position[0], self.__floor_sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        GameManager.remove_entity(self)
        return "Speed"




