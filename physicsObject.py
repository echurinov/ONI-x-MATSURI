import arcade

from component import Component
from entityManager import EntityManager
from eventManager import EventManager


# Component to add physics to an object
# Currently only supports gravity and basic acceleration
class PhysicsObject(Component):
    def __init__(self, uses_gravity=False, max_velocity=(float("inf"), float("inf"))):
        super().__init__("PhysicsObject")
        self.__velocity = (0, 0)
        self.__usesGravity = uses_gravity
        self.__max_velocity = max_velocity
        self.__touching_ground = False
        # Add listener for physics update events
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)
        if uses_gravity:
            # Add listener for gravity update event
            EventManager.add_listener("GravityUpdate", self.on_gravity_update)

    @property
    def touching_ground(self):
        return self.__touching_ground

    @touching_ground.setter
    def touching_ground(self, value):
        self.__touching_ground = value

    @property
    def uses_gravity(self):
        return self.__usesGravity

    # Changes the value of the uses_gravity property, and adds/removes listeners accordingly
    @uses_gravity.setter
    def uses_gravity(self, value):
        self.__usesGravity = value
        if value:
            EventManager.add_listener("GravityUpdate", self.on_gravity_update)
        else:
            EventManager.remove_listener("GravityUpdate", self.on_gravity_update)

    # Adds acceleration to the object
    def add_acceleration(self, acceleration):
        self.__velocity = (self.__velocity[0] + acceleration[0], self.__velocity[1] + acceleration[1])

    def set_velocity(self, velocity):
        self.__velocity = (velocity[0], velocity[1])

    # Runs on each physics update (currently every frame)
    def on_physics_update(self, dt):
        # Clamp velocity
        self.__velocity = (
            arcade.clamp(self.__velocity[0], -self.__max_velocity[0], self.__max_velocity[0]),
            arcade.clamp(self.__velocity[1], -self.__max_velocity[1], self.__max_velocity[1])
        )
        # Get entity transform component
        transform_comp = self.parent.get_component_by_name("Transform")
        # Get entity sprite renderer component
        sprite_comp = self.parent.get_component_by_name("SpriteRenderer")
        # Move the entity
        transform_comp.move((self.__velocity[0] * dt, self.__velocity[1] * dt))

        # Reset the touching ground flag (will be set later if it's on the ground)
        self.__touching_ground = False

        # Check for collisions, move object to the surface if it's inside the floor
        # Only checks for collisions with static entities
        collider_hit_list = arcade.check_for_collision_with_list(sprite_comp.sprite, EntityManager.get_static_entities())
        for collider in collider_hit_list:
            # Get the difference in height between the player and the floor (how far the entity is into the floor)
            # The "parent" attribute is added to the sprite when the SpriteRenderer is added to the entity
            # This parent is the parent entity
            difference = (collider.parent.get_component_by_name("Transform").position[1] + collider.height/2) \
                         - (transform_comp.position[1] - sprite_comp.sprite.height/2)
            # Move the player back up to the floor
            transform_comp.move((0, difference))
            # Set player vertical velocity to 0
            self.set_velocity((self.__velocity[0], 0))
            # Set touching ground to true
            self.__touching_ground = True

    def on_gravity_update(self, gravity, dt):
        self.add_acceleration((0, gravity))
