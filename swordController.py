import arcade

from component import Component
from eventManager import EventManager
from gameManager import GameManager


class SwordController(Component):
    # Called every time physics get updated (currently every frame)
    # Deals with all enemy movement and collision
    def on_physics_update(self, dt):
        player_pos = self.__player_transform.position
        player_vel = self.__player_controller.velocity

        player_left = self.__player_controller.is_moving_left

        direction = -1 if player_left else 1
        self.__transform.position = (player_pos[0] + (35 * direction), player_pos[1])

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):
        #Figured I should keep "movement" of the sword in physics updates
        pass


    def __init__(self):
        super().__init__("SwordController")

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        EventManager.add_listener("Update", self.on_update)
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")
        # Used to get player position and update sword position
        self.__player_transform = GameManager.get_entities_by_name("Player")[0].get_component_by_name("Transform")
        # Used to get player velocity to determine which side the sword entity should be placed on (Velocity may not cover all cases)
        self.__player_controller = GameManager.get_entities_by_name("Player")[0].get_component_by_name("PlayerController")

    # CAN PROBABLY REMOVE THIS
    @property
    def velocity(self):
        return self.__velocity
