import arcade

import enemyController
from component import Component
from eventManager import EventManager
from spriteRenderer import SpriteRenderer
from transform import Transform
from entity import Entity


# A component that handles input for a player
from gameManager import GameManager

# Amount the player is knocked back when they attack
KNOCK_BACK_ATTACK = 350

# Amount the player is knocked back when they take damage
KNOCK_BACK_DAMAGE = 2000

# Timer for attack animation taking precedence over walking animation
ATTACK_TIME = 0.1
ATTACK_COOL_DOWN = 0.2


class PlayerController(Component):
    # Called when a key is pressed
    def on_key_press(self, key, modifiers):
        self.__keys_pressed[key] = True

        # Jump
        if key == arcade.key.W:
            self.__jump_requested = True
            self.__jump_timer = self.__jump_buffer_time
            self.__touching_floor = False

        # Toggle debug
        if key == arcade.key.F:
            GameManager.debug = not GameManager.debug

        # Pause/quit
        if key == arcade.key.ESCAPE:
            arcade.exit()

        # Attacking
        if key == arcade.key.SPACE:
            self.__is_attacking = True


    # Change the value of the key_pressed dictionary when a key is released
    def on_key_release(self, key, modifiers):
        self.__keys_pressed[key] = False

    # Called every time physics get updated (currently every frame)
    # Deals with all player movement and collision
    def on_physics_update(self, dt):
        # Round velocity to 0 if we're close enough
        epsilon = 0.001
        if abs(self.__velocity[0]) < epsilon:
            self.__velocity = (0, self.__velocity[1])
        if abs(self.__velocity[1]) < epsilon:
            self.__velocity = (self.__velocity[0], 0)

        # Update timers
        self.__coyote_timer -= dt
        self.__jump_timer -= dt
        self.__invincibility_timer -= dt
        self.__attack_time -= dt
        self.__attack_timer -= dt
        self.__health_up_timer -= dt
        self.__jumping_timer -= dt
        self.__speed_timer -= dt
        self.__mad_timer -= dt

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

        if self.__transform.position[1] == 0:
            self.__touching_floor = True

        # Get some stuff we'll need
        all_colliders = GameManager.get_colliders()  # List of all colliders in scene
        player_collision_polygon = self.__collider.polygon  # Polygon of the player
        # CAN'T GET THIS OBJECT IN on_created() (CIRCULAR REFERENCE) (Need to create player first in screenView.setup())
        self.__sword_sprite_polygon = GameManager.get_entities_by_name("Sword")[0].get_component_by_name("Collider").polygon


        # Disallow the player from moving past the edge of the screen
        if self.__transform.position[0] <= self.__camera_min + 50:
            self.__transform.position = (self.__camera_min + 51, self.__transform.position[1])


        # Player dies if they fall off the level edge
        if self.__transform.position[1] < -5:
            self.__health = self.__health - 1
            self.__invincibility_timer = 1.0
            arcade.play_sound(self.__damage_sound)
            self.__taking_damage = True
            self.__velocity = (self.__velocity[0] * 490 / 500, self.__velocity[1])
            self.__is_falling = True
            self.__transform.position = (50, self.__camera_min + 55)


        # For when the player is attacking
        if self.__is_attacking and self.__attack_timer < 0:
            arcade.play_sound(self.__attack_sound)
            self.__attack_time = ATTACK_TIME
            self.__attack_timer = ATTACK_COOL_DOWN
            self.__is_attacking = False
            # implement attacking knock back
            if self.__velocity[1] == 0:
                if(self.__velocity[0] >= KNOCK_BACK_ATTACK):
                    self.__velocity = (self.__velocity[0] - KNOCK_BACK_ATTACK, self.__velocity[1])
                elif self.__velocity[0] >= 0:
                    self.__velocity = (self.__velocity[0] - (KNOCK_BACK_ATTACK - (self.__velocity[0] / 2)), self.__velocity[1])
                elif (self.__velocity[0] <= (-1 * KNOCK_BACK_ATTACK)):
                    self.__velocity = (self.__velocity[0] + KNOCK_BACK_ATTACK, self.__velocity[1])
                elif self.__velocity[0] < 0:
                    self.__velocity = (self.__velocity[0] + (KNOCK_BACK_ATTACK - self.__velocity[0] / 2), self.__velocity[1])

            else:
                if(self.__velocity[0] >= KNOCK_BACK_ATTACK):
                    self.__velocity = (self.__velocity[0] - KNOCK_BACK_ATTACK / 2, self.__velocity[1])
                elif self.__velocity[0] >= 0:
                    self.__velocity = (self.__velocity[0] - (KNOCK_BACK_ATTACK / 2 - (self.__velocity[0] / 2)), self.__velocity[1])
                elif (self.__velocity[0] <= (-1 * KNOCK_BACK_ATTACK)):
                    self.__velocity = (self.__velocity[0] + KNOCK_BACK_ATTACK / 2, self.__velocity[1])
                elif self.__velocity[0] < 0:
                    self.__velocity = (self.__velocity[0] + (KNOCK_BACK_ATTACK / 2 - self.__velocity[0] / 2), self.__velocity[1])

            for collider in all_colliders:
                if collider.parent is self:
                    continue
                if "Enemy" in collider.parent.tags:
                    if arcade.are_polygons_intersecting(self.__sword_sprite_polygon, collider.polygon):
                        collider.parent.get_component_by_name("EnemyController").take_damage(self.__attack_power)

        if self.__taking_damage and not self.__is_falling:
            # implement damage knock back
            if self.__velocity[0] >= 0:
                self.__velocity = (self.__velocity[0] - KNOCK_BACK_DAMAGE, self.__velocity[1])
            else:
                self.__velocity = (self.__velocity[0] + KNOCK_BACK_DAMAGE, self.__velocity[1])

        # For when the player is taking damage
        self.__taking_damage = False
        for collider in all_colliders:
            # Ignore the player's own collider
            if collider.parent is self:
                continue
            if "Enemy" in collider.parent.tags:
                if arcade.are_polygons_intersecting(player_collision_polygon, collider.polygon):
                    if self.__invincibility_timer < 0:
                        self.__invincibility_timer = 1.0
                        self.__health = self.__health - 1
                        arcade.play_sound(self.__damage_sound)
                        self.__taking_damage = True
                        self.__velocity = (self.__velocity[0] * 490 / 500, self.__velocity[1])

        if self.__invincibility_timer > 0:
            self.__sprite_renderer.sprite.color = (255, 100, 100)
        else:
            self.__is_falling = False

        if self.__invincibility_timer <= 0 and not self.__health_up and not self.__speed and not self.__jump and not self.__mad:
            self.__sprite_renderer.sprite.color = (255, 255, 255)

        # Two cases here: moving up and moving down
        # Both have different physics and check for different things
        # Deal with vertical movement first, same for both cases (collision checking comes later)
        self.__velocity = (arcade.clamp(self.__velocity[0], -self.__max_velocity[0], self.__max_velocity[0]),
                           arcade.clamp(self.__velocity[1], -self.__max_velocity[1], self.__max_velocity[1]))
        self.__transform.move((0, self.__velocity[1] * dt))

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

                if "PowerUp" in collider.parent.tags:
                    if arcade.are_polygons_intersecting(player_collision_polygon, collider.polygon):
                        temp = collider.parent.on_collection()
                        if temp == "Health-Up":
                            self.__health_up_timer = 0.1
                            self.__sprite_renderer.sprite.color = arcade.color.PINK
                            self.__health_up = True

                        if temp == "Speed":
                            self.__sprite_renderer.sprite.color = (100,100,255)
                            self.__speed = True
                            self.__speed_timer = 5
                            #CHANGE
                            self.__max_velocity = (self.__max_velocity[0] + 350, self.__max_velocity[1] + 350)
                            self.__velocity = (self.__velocity[0] + 100, self.__velocity[1] + 100)

                            #Make player speed

                        if temp == "Jump":
                            self.__jumping_timer = 7
                            self.__jump = True
                            self.__jumping_timer = 7
                            self.__sprite_renderer.sprite.color = (100, 255, 100)
                            #CHANGE
                            self.__gravity = -1000
                            self.__max_velocity = (self.__max_velocity[0], self.__max_velocity[1] + 100)
                            self.__velocity = (self.__velocity[0], self.__velocity[1] + 100)
                            # make player jump high

                        if temp == "Attack":
                            self.__mad = True
                            self.__mad_timer = 5
                            self.__attack_power = 10


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
                        self.__touching_floor = True

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
            arcade.play_sound(self.__jump_sound)
            # print(self.__velocity)
            self.__jump_requested = False
            self.__jump_timer = 0
            self.__touching_ground = False
            self.__touching_floor = False

        # Move the character based on which keys are pressed
        # Deal with wall collision
        # First, move the character horizontally

        self.__transform.move((self.__velocity[0] * dt, 0))
        if self.__keys_pressed[arcade.key.D]:
            self.__moving_left = False
            if self.__velocity[0] > 0:  # Moving right (accelerating)
                self.__velocity = (self.__velocity[0] + self.__horizontal_acceleration * dt, self.__velocity[1])
            else:  # Moving left (decelerating)
                self.__velocity = (self.__velocity[0] + self.__horizontal_turnaround_acceleration * dt, self.__velocity[1])
        elif self.__keys_pressed[arcade.key.A]:
            self.__moving_left = True
            if self.__velocity[0] > 0:  # Moving right (decelerating)
                self.__velocity = (self.__velocity[0] - self.__horizontal_turnaround_acceleration * dt, self.__velocity[1])
            else:  # Moving left (accelerating)
                self.__velocity = (self.__velocity[0] - self.__horizontal_acceleration * dt, self.__velocity[1])
        else:  # no keys pressed, default deceleration
            self.__velocity = (self.__velocity[0] * (1 - self.__horizontal_deceleration_multiplier * dt), self.__velocity[1])

        self.__jump_requested = False

        self.power_up_effects()

    # Gets called every frame
    # dt is the time taken since the last frame
    def on_update(self, dt):
        # Camera Movement Control:
        # 1) Camera does not move vertically
        # 2) Once the character reaches halfway across the screen, the camera moves forward with them again
        # 3) Camera never moves backwards

        width, height = arcade.window_commands.get_display_size()

        if self.__transform.position[0] > (self.__camera_min + width / 2):
            self.__camera_min = self.__camera_min + (self.__transform.position[0] - (self.__camera_min + width / 2))

        GameManager.main_camera.move_to((self.__camera_min, 0), 5 * dt)

        # Animation states
        # If the player is attacking
        attack_timer = self.__attack_time
        if self.__is_attacking:
            self.__animation_frame = 0 # reset animation
            # If the player is in the air
            if not self.__touching_floor:
                if not self.__keys_pressed[arcade.key.A]:
                    self.__animation_state = "jump_attack_R"
                elif not self.__keys_pressed[arcade.key.D]:
                    self.__animation_state = "jump_attack_L"
                else:
                    self.__animation_state = "jump_attack_R"

            # Change attacking animation to be the one of on ground
            if self.__touching_floor:
                if not self.__keys_pressed[arcade.key.A]:
                    self.__animation_state = "attack_R"
                elif not self.__keys_pressed[arcade.key.D]:
                    self.__animation_state = "attack_L"
                else:
                    self.__animation_state = "attack_R"

        elif attack_timer < 0:
            if self.__velocity[0] < 0 and not self.__keys_pressed[arcade.key.A] and not self.__moving_left:
                self.__animation_state = "idle_L"
            elif self.__velocity[0] >= 0 and not self.__keys_pressed[arcade.key.D]:
                self.__animation_state = "idle_R"
            elif self.__keys_pressed[arcade.key.A]:
                self.__animation_state = "walk_L"
            elif self.__keys_pressed[arcade.key.D]:
                self.__animation_state = "walk_R"
            else:
                self.__animation_state = "idle"

        # Animation
        self.__animation_timer += 1
        if self.__animation_timer > self.__animation_data[self.__animation_state]["frame_delay"]:
            # Reset timer
            self.__animation_timer = 0
            # Increment counter
            self.__animation_frame = (self.__animation_frame + 1) % self.__animation_data[self.__animation_state]["num_frames"]
            # Switch sprite
            self.__sprite_renderer.switch_sprite(self.__animation_data[self.__animation_state]["frames"][self.__animation_frame])

        # Health
        self.set_gui()

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
        self.__sword_sprite_polygon = None

        # Private variables for player health
        self.__health = 6
        self.__max_health = 6
        self.__taking_damage = False
        self.__invincibility_timer = 0.0

        #Private variable for player attacking
        self.__is_attacking = False
        self.__attack_time = ATTACK_TIME
        self.__attack_timer = ATTACK_COOL_DOWN
        self.__attack_power = 1

        # Variable used for camera movement, stores the left most edge of the visable screen
        self.__camera_min = 0

        # Variable used for sword positioning, stores the direction the player is facing
        self.__moving_left = False

        # Private variables for player movement
        self.__touching_ground = False
        self.__touching_floor = False #this is a variable just for animation
        self.__jump_requested = False
        self.__velocity = (0, 0)
        self.__gravity = -2000
        self.__jump_speed = 1000
        self.__max_velocity = (500, 2500)
        self.__falling_speed_multiplier = 1.5  # Fall faster than you go up (makes jumps feel better)
        self.__coyote_time = 0.1  # Period after walking off a platform where you can still jump (another QOL feature)
        self.__coyote_timer = 0  # Temporary variable to keep track of the coyote time
        self.__is_falling = False # variable changes to true once you fall off an edge and false once you respawn

        # Pressing jump within this amount of time before touching the ground
        # will make you jump when you land, avoiding missed inputs.
        self.__jump_buffer_time = 0.1
        self.__jump_timer = 0

        # Variables for the powerups
        self.__health_up = False
        self.__speed = False
        self.__jump = False
        self.__mad = False

        self.__power_up_type = None
        self.__health_up_timer = 0.5
        self.__speed_timer = 7
        self.__jumping_timer = 7
        self.__mad_timer = 5

        self.__flash_count = 0

        self.__horizontal_acceleration = 700  # How quickly you accelerate when moving sideways
        self.__horizontal_deceleration_multiplier = 10  # How quickly you decelerate when no button is pressed
        self.__horizontal_turnaround_acceleration = 4000  # How quickly you decelerate when changing direction


        # Sprite switching (animation)
        self.__animation_timer = 0  # Frames since last change
        self.__animation_frame = 0  # Which frame we're in
        self.__animation_state = "idle"
        # Dictionary for frames for animations

        self.__exit_sprite = arcade.Sprite("assets/sprites/pause.png", 1.0)

        self.__animation_data = {
            "idle_L": {
                "name_prefix": "player_idle_L_",  # Prefix for the filenames of the animation (not including the number)
                "num_frames": 2,  # Numbers of frames in the animation
                "frame_delay": 30,  # Frames between animation frames
                "frames": []  # All the sprites, loaded at runtime
            },
            "idle_R": {
                "name_prefix": "player_idle_R_",
                "num_frames": 2,
                "frame_delay": 30,
                "frames": []
            },
            "idle": {
                "name_prefix": "player_idle_",
                "num_frames": 2,
                "frame_delay": 30,
                "frames": []
            },
            "walk_L": {
                "name_prefix": "player_walk_L_",
                "num_frames": 4,
                "frame_delay": 5,
                "frames": []
            },
            "walk_R": {
                "name_prefix": "player_walk_R_",
                "num_frames": 4,
                "frame_delay": 5,
                "frames": []
            },
            "attack_L": {
                "name_prefix": "player_attack_L_",  # Prefix for the filenames of the animation (not including the number)
                "num_frames": 2,  # Numbers of frames in the animation
                "frame_delay": 5,  # Frames between animation frames
                "frames": []  # All the sprites, loaded at runtime
            },
            "attack_R": {
                "name_prefix": "player_attack_R_",
                "num_frames": 2,
                "frame_delay": 5,
                "frames": []
            },
            "jump_attack_L": {
                "name_prefix": "player_jump_attack_L_",
                "num_frames": 2,
                "frame_delay": 5,
                "frames": []
            },
            "jump_attack_R": {
                "name_prefix": "player_jump_attack_R_",
                "num_frames": 2,
                "frame_delay": 5,
                "frames": []
            }
        }
        for animation_name, animation in self.__animation_data.items():
            for i in range(animation["num_frames"]):
                animation["frames"].append(arcade.Sprite("assets/sprites/player/" + animation["name_prefix"] + str(i+1) +".png", 0.5))

        # Add listeners for all the events
        EventManager.add_listener("Update", self.on_update)  # calls on_update every frame
        EventManager.add_listener("KeyPress", self.on_key_press)  # calls on_key_press every time a key is pressed
        EventManager.add_listener("KeyRelease",
                                  self.on_key_release)  # calls on_key_release every time a key is released
        EventManager.add_listener("PhysicsUpdate", self.on_physics_update)  # calls physics_update every frame

        # Load sounds
        self.__attack_sound = arcade.load_sound("assets/sounds/player/player_attack.wav")
        self.__damage_sound = arcade.load_sound("assets/sounds/player/player_damage.wav")
        self.__jump_sound = arcade.load_sound("assets/sounds/player/player_jump3.wav")

    def set_health(self, health):
        self.__health = health

    def set_power_up(self, power_up):
        self.__power_up_type = power_up

    # Called when parent entity is created
    def on_created(self):
        self.__collider = self.parent.get_component_by_name("Collider")
        self.__transform = self.parent.get_component_by_name("Transform")
        self.__sprite_renderer = self.parent.get_component_by_name("SpriteRenderer")

    def set_gui(self):
        GameManager.clear_gui_sprite()

        # Exit Button
        exit_sprite_renderer = SpriteRenderer(self.__exit_sprite)
        exit_transform = Transform((1460, 750 + self.__exit_sprite.height / 2), 0, 1.0)
        exit_entity = Entity("Exit", ["ExitTag"], [exit_sprite_renderer, exit_transform])
        GameManager.add_gui_entity(exit_entity)

        if self.__health <= 2:
            if self.__health == 1:
                self.make_heart_entity(0, "half")
            else:
                self.make_heart_entity(0, "full")
            self.make_heart_entity(1, "empty")
            self.make_heart_entity(2, "empty")
        elif self.__health <= 4:
            if self.__health == 3:
                self.make_heart_entity(1, "half")
            else:
                self.make_heart_entity(1, "full")
            self.make_heart_entity(0, "full")
            self.make_heart_entity(2, "empty")
        else:
            if self.__health == 5:
                self.make_heart_entity(2, "half")
            else:
                self.make_heart_entity(2, "full")
            self.make_heart_entity(0, "full")
            self.make_heart_entity(1, "full")

    def make_heart_entity(self, num_heart, state):
        if state == "full":
            heart_sprite = arcade.Sprite("assets/sprites/heart_full.png", 1.0)
        elif state == "half":
            heart_sprite = arcade.Sprite("assets/sprites/heart_half.png", 1.0)
        else:
            heart_sprite = arcade.Sprite("assets/sprites/heart_empty.png", 1.0)

        heart_sprite_renderer = SpriteRenderer(heart_sprite)
        heart_transform = Transform((num_heart * (heart_sprite.width + 10) + 70, 750 + heart_sprite.height / 2), 0, 1.0)
        heart_entity = Entity("Heart", ["HeartTag"], [heart_sprite_renderer, heart_transform])
        GameManager.add_gui_entity(heart_entity)

    def get_exit_sprite(self):
        return self.__exit_sprite

    def set_exit_sprite(self, new_sprite):
        self.__exit_sprite = new_sprite

    def power_up_effects(self):


        # FLASHES PINK when you get HEALTH-UP
        if self.__health_up_timer < 0 and self.__flash_count == 0 and self.__health_up:
            self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__health_up_timer = 0.1
            self.__flash_count += 1

        if self.__health_up_timer < 0 and self.__flash_count == 1 and self.__health_up:
            self.__sprite_renderer.sprite.color = arcade.color.PINK
            self.__health_up_timer = 0.1
            self.__flash_count += 1

        if self.__health_up_timer < 0 and self.__flash_count == 2 and self.__health_up:
            self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__flash_count = 0
            self.__health_up = False

        # Undoes the effect of the speed-boost power-up
        if self.__speed_timer < 0 and self.__speed:
            self.__speed = False
            self.__flash_count = 0
            self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__max_velocity = (self.__max_velocity[0] - 350, self.__max_velocity[1] - 350)

        # Undoes the effect of the jump power-up
        if self.__jumping_timer < 0 and self.__jump:
            self.__jump = False
            self.__flash_count = 0
            self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__gravity = -1700
            self.__max_velocity = (self.__max_velocity[0], self.__max_velocity[1] - 100)
            self.__velocity = (self.__velocity[0], self.__velocity[1] - 100)

        # Undoes the effect of the attack power-up
        if self.__mad_timer < 0 and self.__mad:
            self.__mad = False
            self.__flash_count = 0
            self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__attack_power = 1

        # FLASHES BLUE when you get SPEED-BOOST
        if self.__speed:
            if self.__flash_count % 16 == 0:
                self.__sprite_renderer.sprite.color = (100, 100, 255)
            elif self.__flash_count % 8 == 0:
                self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__flash_count = (self.__flash_count + 1) % 80

        # FLASHES GREEN when you get JUMP-BOOST
        if self.__jump:
            if self.__flash_count % 16 == 0:
                self.__sprite_renderer.sprite.color = (100, 255, 100)
            elif self.__flash_count % 8 == 0:
                self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__flash_count = (self.__flash_count + 1) % 80

        # FLASHES PURPLE when you get ATTACK-BOOST
        if self.__mad:
            if self.__flash_count % 16 == 0:
                self.__sprite_renderer.sprite.color = (255, 100, 255)
            elif self.__flash_count % 8 == 0:
                self.__sprite_renderer.sprite.color = (255, 255, 255)
            self.__flash_count = (self.__flash_count + 1) % 80


    @property
    def touching_ground(self):
        return self.__touching_ground

    @property
    def velocity(self):
        return self.__velocity

    @property
    def health(self):
        return self.__health

    @property
    def max_health(self):
        return self.__max_health

    @property
    def taking_damage(self):
        return self.__taking_damage

    @property
    def is_attacking(self):
        return self.__is_attacking

    @property
    def is_moving_left(self):
        return self.__moving_left

    @property
    def attack_power(self):
        return self.__attack_power