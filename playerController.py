import arcade

from component import Component
from eventManager import EventManager

# A component that handles input for a player
from gameManager import GameManager


class PlayerController(Component):
    # Called when a key is pressed
    def on_key_press(self, key, modifiers):
        self.__keys_pressed[key] = True

        # Jump
        if key == arcade.key.W:
            self.__jump_requested = True
            self.__jump_timer = self.__jump_buffer_time

        # Toggle debug
        if key == arcade.key.F:
            GameManager.debug = not GameManager.debug

    # Change the value of the key_pressed dictionary when a key is released
    def on_key_release(self, key, modifiers):
        self.__keys_pressed[key] = False

    # Called every time physics get updated (currently every frame)
    # Deals with all player movement and collision
    def on_physics_update(self, dt):

        # Update timers
        self.__coyote_timer -= dt
        self.__jump_timer -= dt

        # If the player is in the air, determine if they've landed on the ground
        # If the player is on the ground, determine if they've jumped (or moved up/down a slope)
        # In both cases, determine if they've collided with a wall

        # On-the-ground case
        # Deal with whether the player should fall (they've stepped off the platform) and jumps
        if self.__touching_ground:
            # Give player slight downward movement so that the downward case below is run
            self.__velocity = (self.__velocity[0], -0.1)
            self.__touching_ground = False
            self.__coyote_timer = self.__coyote_time  # Start coyote timer

        # Get some stuff we'll need
        all_colliders = GameManager.get_colliders()  # List of all colliders in scene
        player_collision_polygon = self.__collider.polygon  # Polygon of the player

        # Two cases here: moving up and moving down
        # Both have different physics and check for different things
        # Deal with vertical movement first, same for both cases (collision checking comes later)
        self.__velocity = (arcade.clamp(self.__velocity[0], -self.__max_velocity[0], self.__max_velocity[0]),
                           arcade.clamp(self.__velocity[1], -self.__max_velocity[1], self.__max_velocity[1]))
        self.__transform.move((0, self.__velocity[1]))

        # First case: moving up
        # Check for ground collision (with ceilings)
        # Deal with vertical deceleration
        if self.__velocity[1] > 0:
            # Ground collision (ceilings)
            largest_difference = float("inf")
            for collider in all_colliders:
                # Ignore the player's own collider
                if collider.parent is self:
                    continue
                # Ignore colliders that we're above (avoid colliding with floor we just left)
                # TODO: THIS IS A BODGE
                if self.__transform.position[1] > collider.transform.position[1]:
                    continue
                # Only checking for objects tagged with "Ground" (solid objects, not platforms)
                if "Ground" in collider.parent.tags:
                    if arcade.are_polygons_intersecting(player_collision_polygon, collider.polygon):
                        # Get how far we would have to move the player to get them out of the ceiling
                        difference = (collider.transform.position[1] - collider.height / 2) - (
                                self.__transform.position[1] + self.__collider.height / 2)
                        if difference < largest_difference:  # Largest negative amount
                            largest_difference = difference
                        # Stop the player's vertical movement
                        self.__velocity = (self.__velocity[0], 0)
            # Move the player out of the ceiling if they're in it
            if largest_difference != float("inf"):
                self.__transform.move((0, largest_difference))

            # Deal with vertical deceleration
            self.__velocity = (self.__velocity[0], self.__velocity[1] + (self.__gravity * dt))

        # Second case: moving down
        # Check for collision with ground and platforms
        # Deal with vertical acceleration
        else:
            # Ground collision (floors)
            largest_difference = float("-inf")
            for collider in all_colliders:
                # Ignore the player's own collider
                if collider.parent is self:
                    continue
                # Only checking for objects tagged with "Ground" or "Platform" (solid objects and platforms)
                if "Ground" in collider.parent.tags or "Platform" in collider.parent.tags:
                    if arcade.are_polygons_intersecting(player_collision_polygon, collider.polygon):
                        # Get how far we would have to move the player to get them out of the floor
                        difference = (collider.transform.position[1] + collider.height / 2) - \
                                     (self.__transform.position[1] - self.__collider.height / 2)

                        if difference > largest_difference:
                            largest_difference = difference
                        # Stop the player's vertical movement
                        self.__velocity = (self.__velocity[0], 0)
                        # Set the touching_ground flag
                        self.__touching_ground = True
            # Move the player out of the floor if they're in it
            if largest_difference != float("-inf"):
                self.__transform.move((0, largest_difference))

            # Deal with vertical acceleration
            # Multiply vertical acceleration by a multiplier to get faster falling (less "floaty")
            self.__velocity = (
                self.__velocity[0], self.__velocity[1] + (self.__gravity * self.__falling_speed_multiplier * dt))

        # If we're on the ground (or in coyote time) and the player has pressed the jump button, let them jump
        if (self.__jump_requested or self.__jump_timer > 0) and (self.__touching_ground or self.__coyote_timer > 0):
            self.__velocity = (self.__velocity[0], self.__jump_speed)
            # print(self.__velocity)
            self.__jump_requested = False
            self.__jump_timer = 0
            self.__touching_ground = False

        # Move the character based on which keys are pressed
        # Deal with wall collision
        # First, move the character horizontally

        self.__transform.move((self.__velocity[0], 0))
        if self.__keys_pressed[arcade.key.D]:
            if self.__velocity[0] > 0:  # Moving right (accelerating)
                self.__velocity = (self.__velocity[0] + self.__horizontal_acceleration * dt, self.__velocity[1])
            else:  # Moving left (decelerating)
                self.__velocity = (self.__velocity[0] + self.__horizontal_turnaround_acceleration * dt, self.__velocity[1])
        elif self.__keys_pressed[arcade.key.A]:
            if self.__velocity[0] > 0:  # Moving right (decelerating)
                self.__velocity = (self.__velocity[0] - self.__horizontal_turnaround_acceleration * dt, self.__velocity[1])
            else:  # Moving left (accelerating)
                self.__velocity = (self.__velocity[0] - self.__horizontal_acceleration * dt, self.__velocity[1])
        else:  # no keys pressed, default deceleration
            self.__velocity = (self.__velocity[0] * (1 - self.__horizontal_deceleration_multiplier * dt), self.__velocity[1])

        self.__jump_requested = False

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):

        # Scroll the screen so the player stays in the center
        GameManager.main_camera.move_to(
            (self.__transform.position[0] - GameManager.SCREEN_WIDTH / 2,
             self.__transform.position[1] - GameManager.SCREEN_HEIGHT / 2),
            5 * dt)

    def __init__(self):
        super().__init__("PlayerController")
        # Initialize the keys_pressed dictionary
        self.__keys_pressed = {
            arcade.key.A: False,
            arcade.key.D: False
        }

        # Store some components here (set when the program starts), so we don't have to look for them each time
        self.__transform = None
        self.__collider = None
        self.__sprite_renderer = None

        # Private variables for player movement
        self.__touching_ground = False
        self.__jump_requested = False
        self.__velocity = (0, 0)
        self.__gravity = -50
        self.__jump_speed = 25
        self.__max_velocity = (100, 100)
        self.__falling_speed_multiplier = 1.5  # Fall faster than you go up (makes jumps feel better)
        self.__coyote_time = 0.1  # Period after walking off a platform where you can still jump (another QOL feature)
        self.__coyote_timer = 0  # Temporary variable to keep track of the coyote time

        # Pressing jump within this amount of time before touching the ground
        # will make you jump when you land, avoiding missed inputs.
        self.__jump_buffer_time = 0.1
        self.__jump_timer = 0

        self.__horizontal_acceleration = 10  # How quickly you accelerate when moving sideways
        self.__horizontal_deceleration_multiplier = 10  # How quickly you decelerate when no button is pressed
        self.__horizontal_turnaround_acceleration = 200  # How quickly you decelerate when changing direction

        # Add listeners for all the events
        EventManager.add_listener("Update", self.on_update)  # calls on_update every frame
        EventManager.add_listener("KeyPress", self.on_key_press)  # calls on_key_press every time a key is pressed
        EventManager.add_listener("KeyRelease",
                                  self.on_key_release)  # calls on_key_release every time a key is released
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")

    @property
    def touching_ground(self):
        return self.__touching_ground
