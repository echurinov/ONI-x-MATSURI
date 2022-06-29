import arcade

from component import Component
from eventManager import EventManager

# Component to add physics to an object
# Currently only supports gravity and basic acceleration
class PhysicsObject(Component):
    def __init__(self, uses_gravity=False, max_velocity=(float("inf"), float("inf"))):
        super().__init__("PhysicsObject")
        self.__velocity = (0, 0)
        self.__usesGravity = uses_gravity
        self.__max_velocity = max_velocity
        # Add listener for physics update events
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)
        if uses_gravity:
            # Add listener for gravity update event
            EventManager.add_listener("GravityUpdate", self.on_gravity_update)

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
        player_ent = self.parent
        transform_comp = player_ent.get_component_by_name("Transform")
        transform_comp.move((self.__velocity[0] * dt, self.__velocity[1] * dt))

    def on_gravity_update(self, gravity, dt):
        self.add_acceleration((0, gravity))
