import arcade

from component import Component
from eventManager import EventManager


# A component that handles input for a player
class PlayerController(Component):
    # Called when a key is pressed
    def on_key_press(self, key, modifiers):
        self.__keys_pressed[key] = True

        # Jump
        if key == arcade.key.W:
            self.parent.get_component_by_name("PhysicsObject").set_velocity((0, 250))

    # Change the value of the key_pressed dictionary when a key is released
    def on_key_release(self, key, modifiers):
        self.__keys_pressed[key] = False

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):
        # Get the transform component from the player object
        player_ent = self.parent
        transform_comp = player_ent.get_component_by_name("Transform")
        # Move the character based on which keys are pressed
        if self.__keys_pressed[arcade.key.A]:
            transform_comp.move((-50 * dt, 0))
        if self.__keys_pressed[arcade.key.D]:
            transform_comp.move((50 * dt, 0))

    def __init__(self):
        super().__init__("PlayerController")
        # Initialize the keys_pressed dictionary
        self.__keys_pressed = {
            arcade.key.A: False,
            arcade.key.D: False
        }

        # Add listeners for all the events
        EventManager.add_listener("Update", self.on_update)  # calls on_update every frame
        EventManager.add_listener("KeyPress", self.on_key_press)  # calls on_key_press every time a key is pressed
        EventManager.add_listener("KeyRelease",
                                  self.on_key_release)  # calls on_key_release every time a key is released
