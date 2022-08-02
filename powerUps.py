import arcade

from collider import Collider
from entity import Entity
from spriteRenderer import SpriteRenderer
from transform import Transform
from eventManager import EventManager
from gameManager import GameManager
from soundManager import SoundManager

BOUNCE_TIME = 0.3
BOUNCE_AMOUNT = 7


class PowerUpHealth(Entity):
    def __init__(self, position):
        self.__sprite = arcade.Sprite("assets/sprites/cottoncandy.png")
        sprite_renderer = SpriteRenderer(self.__sprite)
        transform = Transform(position, 0)
        collider = Collider(auto_generate_polygon="box")
        super(PowerUpHealth, self).__init__("PowerUpHealth", ["PowerUp"], [sprite_renderer, transform, collider],
                                            static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__collection_timer = 0.3

        self.__player_controller = None  # Will set this later

    # Avoid memory leak
    # If this is in init, it will mess with the copying when level sections are being loaded and unloaded
    def on_created(self):
        if self.in_scene:
            EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)

    def on_physics_update(self, dt):
        self.__collection_timer -= dt
        if self.__collection_timer < 0:
            self.__color_done = True
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__sprite.set_position(self.__sprite.position[0],
                                       self.__sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        if self.__player_controller is None:
            self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
                "PlayerController")
        if self.__player_controller.health < self.__player_controller.max_health:
            self.__player_controller.set_health(self.__player_controller.health + 1)

        SoundManager.play_sound("powerups", "heal")
        GameManager.remove_entity(self)
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        return "Health-Up"


class PowerUpSpeed(Entity):
    def __init__(self, position):
        self.__sprite = arcade.Sprite("assets/sprites/onigiri.png")
        sprite_renderer = SpriteRenderer(self.__sprite)
        transform = Transform(position, 0)
        collider = Collider(auto_generate_polygon="box")
        super(PowerUpSpeed, self).__init__("PowerUpSpeed", ["PowerUp"],
                                           [sprite_renderer, transform, collider],
                                           static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__player_controller = None

    # Avoid memory leak
    # If this is in init, it will mess with the copying when level sections are being loaded and unloaded
    def on_created(self):
        if self.in_scene:
            EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)

    def on_physics_update(self, dt):
        if self.__player_controller is None:
            self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
                "PlayerController")
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__sprite.set_position(self.__sprite.position[0],
                                       self.__sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        GameManager.remove_entity(self)
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        return "Speed"


class PowerUpJump(Entity):
    def __init__(self, position):
        self.__sprite = arcade.Sprite("assets/sprites/squid.png")
        sprite_renderer = SpriteRenderer(self.__sprite)
        transform = Transform(position, 0)
        collider = Collider(auto_generate_polygon="box")
        super(PowerUpJump, self).__init__("PowerUpJump", ["PowerUp"],
                                          [sprite_renderer, transform, collider],
                                          static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__player_controller = None

    # Avoid memory leak
    # If this is in init, it will mess with the copying when level sections are being loaded and unloaded
    def on_created(self):
        if self.in_scene:
            EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)

    def on_physics_update(self, dt):
        if self.__player_controller is None:
            self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
                "PlayerController")
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__sprite.set_position(self.__sprite.position[0],
                                       self.__sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        GameManager.remove_entity(self)
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        return "Jump"


class PowerUpAttack(Entity):
    def __init__(self, position):
        self.__sprite = arcade.Sprite("assets/sprites/dango.png")
        sprite_renderer = SpriteRenderer(self.__sprite)
        transform = Transform(position, 0)
        collider = Collider(auto_generate_polygon="box")
        super(PowerUpAttack, self).__init__("PowerUpAttack", ["PowerUp"],
                                            [sprite_renderer, transform, collider],
                                            static=False)
        self.__position = position
        self.__bounce_timer = BOUNCE_TIME
        self.__bounce_amount = BOUNCE_AMOUNT

        self.__player_controller = None

    # Avoid memory leak
    # If this is in init, it will mess with the copying when level sections are being loaded and unloaded
    def on_created(self):
        if self.in_scene:
            EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

    def on_remove(self):
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)

    def on_physics_update(self, dt):
        if self.__player_controller is None:
            self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name(
                "PlayerController")
        self.__bounce_timer -= dt
        if self.__bounce_timer < 0:
            self.__bounce_timer = BOUNCE_TIME
            self.__bounce_amount = self.__bounce_amount * -1
            self.__sprite.set_position(self.__sprite.position[0],
                                       self.__sprite.position[1] + self.__bounce_amount)

    def on_collection(self):
        GameManager.remove_entity(self)
        EventManager.remove_listener("PhysicsUpdate", self.on_physics_update)
        return "Attack"
